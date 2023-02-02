from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon_ru import LEXICON


# Create pagination keyboard function
def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    pagination_kb = InlineKeyboardMarkup()

    pagination_kb.row(*[InlineKeyboardButton(LEXICON[button] if button in LEXICON else button,
                                             callback_data=button) for button in buttons])
    return pagination_kb
