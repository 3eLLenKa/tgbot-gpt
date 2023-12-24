from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import flags
from aiogram.fsm.context import FSMContext
from aiogram.methods.get_chat_member import GetChatMember

from states import Gen

import utils
import text
import kb
import db

router = Router()

@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message, state: FSMContext):
    await state.set_state(Gen.menu_state)
    await msg.answer(text.menu, reply_markup=kb.menu)
    await msg.delete_reply_markup()

@router.callback_query(F.data == "menu")
async def menu(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.menu_state)
    await clbck.message.edit_text(text.menu, reply_markup=kb.menu)

@router.message(Command("menu"))
async def menu(msg: Message, state: FSMContext):
    await state.set_state(Gen.menu_state)
    await msg.answer(text.menu, reply_markup=kb.menu)

@router.message(Command("profile"))
async def menu(msg: Message, state: FSMContext):
    await state.set_state(Gen.menu_state)
    await msg.answer(text.profile.format(name=msg.from_user.first_name, questions=str(await db.GetQuestionsCount(msg.from_user.id)), tokens=str(await db.GetTokens(msg.from_user.id)), days=str(await db.GetResetTokensTime(msg.from_user.id)), model=str(await db.GetModel(msg.from_user.id)), balance=str(await db.GetBalance(msg.from_user.id))), reply_markup=kb.iexit_kb)

@router.message(Command("start", "restart"))
async def start_handler(msg: Message):
    await db.registration(msg.from_user.id)
    await msg.answer(text.greetings.format(name=msg.from_user.first_name), reply_markup=kb.menu)
    utils.history[msg.from_user.id] = []

@router.message(Command("help"))
async def help_command_msg(msg: Message):
    await msg.answer(text.help, reply_markup=kb.iexit_kb)

@router.callback_query(F.data == "help")
async def help_msg(clbck: CallbackQuery):
    await clbck.message.edit_text(text.help, reply_markup=kb.iexit_kb)

@router.callback_query(F.data == "model") # Тут будем делать проверку на текущую модель в БД
async def model_choice_msg(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.menu_state)
    
    if await db.GetModel(clbck.from_user.id) == 'gpt-3.5-turbo-1106':
        await clbck.message.edit_text(text.model, reply_markup=kb.gpt3)
    if await db.GetModel(clbck.from_user.id) == 'gpt-4-vision-preview':
        await clbck.message.edit_text(text.model, reply_markup=kb.gpt4)
    # ...

@router.callback_query(F.data == "gpt3") # Выбор модели gpt-3.5-turbo
async def model_gpt3_msg(clbck: CallbackQuery):
    await db.UpdateTextData(clbck.from_user.id, "Model", "gpt-3.5-turbo-1106")
    await clbck.message.edit_text(text.model, reply_markup=kb.gpt3)

@router.callback_query(F.data == "gpt4") # Выбор модели GPT-4 (Будем делать проверку на наличие подписки)
async def model_gpt4_msg(clbck: CallbackQuery):
    if await db.GetSubscribe(clbck.from_user.id) == "Активна":
        await db.UpdateTextData(clbck.from_user.id, "Model", "gpt-4-vision-preview")
        await clbck.message.edit_text(text.model, reply_markup=kb.gpt4)
    else:
        await clbck.message.answer(text.no_subscribe)
    # ...

@router.callback_query(F.data == "generate_text")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.text_prompt)
    await clbck.message.edit_text(text.gen_text)
    await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)

@router.message(Gen.text_prompt)
@flags.chat_action("typing")
async def generate_text(msg: Message):
    tokens = await db.GetTokens(msg.from_user.id)
    questions = await db.GetQuestionsCount(msg.from_user.id)
    prompt = msg.text
    mesg = await msg.answer(text.gen_wait)
    model = await db.GetModel(msg.from_user.id)

    if model == "gpt-3.5-turbo-1106":
        res = await utils.generate_text(prompt, msg.from_user.id, model)
    else:
        res = await utils.generate_text(prompt, msg.from_user.id, model.lower())

    if not res:
        return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
    await mesg.edit_text(res, reply_markup=kb.reset_context)

    tokens = tokens - len(prompt)
    questions += 1

    utils.history[msg.from_user.id].insert(0, {"role": "assistant", "content": res})
    utils.history[msg.from_user.id].insert(0, {"role": "user", "content": prompt})

    await db.UpdateData(msg.from_user.id, "Tokens", tokens)
    await db.UpdateData(msg.from_user.id, "QuestionsCount", questions)

    print(utils.history)

@router.callback_query(F.data == "reset")
async def reset(msg: Message):
    await utils.reset_context(msg.from_user.id)
    await msg.answer(text.reset_context)

@router.callback_query(F.data == "free_tokens")
async def free_tokens(clbck: CallbackQuery):
    await clbck.message.edit_text(text.free_tokens, reply_markup=kb.subscribe_channel)

@router.callback_query(F.data == 'check_subscribe')
async def check_subscribe(msg: Message):
    if await utils.check_subscribe(GetChatMember(chat_id='@msk_live', user_id=msg.from_user.id)):
        await msg.answer(text.grant)

@router.callback_query(F.data == "tokens")
async def buy_tokens(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.buy_tokens)
    await clbck.message.edit_text(text.buy_tokens, reply_markup=kb.iexit_kb)

@router.message(Gen.buy_tokens)
async def buy_tokens(msg: Message):
    user_price = msg.text

    if user_price.isdigit():

        if int(user_price) < 100:
            await msg.answer(text.minimum_tokens)
        elif int(user_price) > 100000:
            await msg.answer(text.maximum_tokens)
        else:
            await msg.answer(text.tokens_price.format(price=int(user_price) * 0.01), reply_markup=kb.buy_tokens)
    else:
        await msg.answer(text.no_digit)

@router.callback_query(F.data == "buy_tokens")
async def buy(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.menu_state)
    await clbck.message.answer("*Тут должна быть ссылка на оплату*")

@router.callback_query(F.data == "balance")
async def buy_tokens(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.top_balance)
    await clbck.message.edit_text(text.top_balance, reply_markup=kb.iexit_kb)

@router.message(Gen.top_balance)
async def buy_tokens(msg: Message):
    user_price = msg.text

    if user_price.isdigit():

        if int(user_price) < 50:
            await msg.answer(text.minimum_balance)
        elif int(user_price) > 1000:
            await msg.answer(text.maximum_balance)
        else:
            await msg.answer(text.balance_price.format(price=int(user_price)), reply_markup=kb.top_balance)
    else:
        await msg.answer(text.no_digit)

@router.callback_query(F.data == "top_balance")
async def buy(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.menu_state)
    await clbck.message.answer("*Тут должна быть ссылка на оплату*")