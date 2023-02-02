from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove


# Echo handler
async def send_echo(message: Message):
    await message.answer(f'Это эхо! {message.text}', reply_markup=ReplyKeyboardRemove())


# Register echo handler
def register_echo_handler(dp: Dispatcher):
    dp.register_message_handler(send_echo)