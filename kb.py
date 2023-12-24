from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

menu = [
    [InlineKeyboardButton(text="📝 ChatGPT", callback_data="generate_text"),
    InlineKeyboardButton(text="🖼 DALL-E 3", callback_data="generate_image")],
    [InlineKeyboardButton(text="💳 Купить токены", callback_data="tokens"),
    InlineKeyboardButton(text="💰 Пополнить баланс", callback_data="balance")],
    [InlineKeyboardButton(text="🤖 Выбрать модель", callback_data="model"),
    InlineKeyboardButton(text="🎁 Бесплатные токены", callback_data="free_tokens")],
    [InlineKeyboardButton(text="🔎 Помощь", callback_data="help")]
]

iexit_button = [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]

menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True, one_time_keyboard=True)
gpt3 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="gpt-3.5-turbo ✅", callback_data='gpt3'), InlineKeyboardButton(text="GPT-4", callback_data='gpt4')], [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
gpt4 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="gpt-3.5-turbo", callback_data='gpt3'), InlineKeyboardButton(text="GPT-4 ✅", callback_data='gpt4')], [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
reset_context = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Очистить историю диалога", callback_data='reset')]])
subscribe_channel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Подписаться", url='https://t.me/msk_live'), InlineKeyboardButton(text="Проверить", callback_data="check_subscribe")], [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
buy_tokens = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💳 Оплатить", callback_data="buy_tokens")], [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
top_balance = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💳 Оплатить", callback_data="top_balance")], [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
