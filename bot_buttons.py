from aiogram.types import ReplyKeyboardMarkup


def open_menu_def():
    menu_default = ReplyKeyboardMarkup(resize_keyboard=True)
    menu_default.row("✉️Send all", "💬 Chat list")
    return menu_default
