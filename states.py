from aiogram.fsm.state import StatesGroup, State

class Gen(StatesGroup):
    text_prompt = State()
    img_prompt = State()
    menu_state = State()
    buy_tokens = State()
    top_balance = State()