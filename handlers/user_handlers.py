from copy import deepcopy

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from database.database import user_dict_template, user_db
from keyboards.bookmarks import create_bookmarks_keyboard, create_edit_keyboard
from keyboards.pagination import create_pagination_keyboard
from lexicon.lexicon_ru import LEXICON
from services.file_handling import book


# /start handler + add user to database
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = deepcopy(user_dict_template)


# /help handler
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# /beginning handler that send first page
async def process_beginning_command(message: Message):
    user_db[message.from_user.id]['page'] = 1
    text = book[user_db[message.from_user.id]['page']]
    await message.answer(text=text, reply_markup=create_pagination_keyboard('backward',
                                                                            f'{user_db[message.from_user.id]["page"]}/{len(book)}',
                                                                            'forward'))


# /continue handler that send last page where user stopped
async def process_continue_command(message: Message):
    text = book[user_db[message.from_user.id]['page']]
    await message.answer(text=text, reply_markup=create_pagination_keyboard('backward',
                                                                            f'{user_db[message.from_user.id]["page"]}/{len(book)}',
                                                                            'forward'))


# /bookmarks handler that show to user his bookmarks
async def process_bookmarks_command(message: Message):
    if user_db[message.from_user.id]['bookmarks']:
        await message.answer(text=LEXICON[message.text],
                             reply_markup=create_bookmarks_keyboard(*user_db[message.from_user.id]['bookmarks']))
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


# forward button
async def process_forward_press(callback: CallbackQuery):
    if user_db[callback.from_user.id]['page'] < len(book):
        user_db[callback.from_user.id]['page'] += 1
        text = book[user_db[callback.from_user.id]['page']]
        await callback.message.edit_text(text=text,
                                         reply_markup=create_pagination_keyboard('backward',
                                                                                 f'{user_db[callback.from_user.id]["page"]}/{len(book)}',
                                                                                 'forward'))
    await callback.answer()


# backward button
async def process_backward_press(callback: CallbackQuery):
    if user_db[callback.from_user.id]['page'] > 1:
        user_db[callback.from_user.id]['page'] -= 1
        text = book[user_db[callback.from_user.id]['page']]
        await callback.message.edit_text(text=text,
                                         reply_markup=create_pagination_keyboard('backward',
                                                                                 f'{user_db[callback.from_user.id]["page"]}/{len(book)}',
                                                                                 'forward'))
    await callback.answer()


# page button that add current page in bookmarks
async def process_page_press(callback: CallbackQuery):
    user_db[callback.from_user.id]['bookmarks'].add(user_db[callback.from_user.id]['page'])
    await callback.answer('Страница добавлена в закладки!')


# inline bookmark button
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    user_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(text=text,
                                     reply_markup=create_pagination_keyboard('backward',
                                                                             f'{user_db[callback.from_user.id]["page"]}/{len(book)}',
                                                                             'forward'))
    await callback.answer()


# edit button
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON[callback.data],
                                     reply_markup=create_edit_keyboard(*user_db[callback.from_user.id]['bookmarks']))
    await callback.answer()


# cancel button
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


# delete bookmark
async def process_delete_bookmark_press(callback: CallbackQuery):
    user_db[callback.from_user.id]['bookmarks'].remove(int(callback.data[:-3]))

    if user_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(text=LEXICON['/bookmarks'],
                                         reply_markup=create_bookmarks_keyboard(
                                             *user_db[callback.from_user.id]['bookmarks']))
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
    await callback.answer()


# register all handlers
def register_user_handlers(dp: Dispatcher):
    # message handlers
    dp.register_message_handler(process_start_command, commands=['start'])
    dp.register_message_handler(process_help_command, commands=['help'])
    dp.register_message_handler(process_beginning_command, commands=['beginning'])
    dp.register_message_handler(process_continue_command, commands=['continue'])
    dp.register_message_handler(process_bookmarks_command, commands=['bookmarks'])
    # callback handlers
    dp.register_callback_query_handler(process_forward_press, text='forward')
    dp.register_callback_query_handler(process_backward_press, text='backward')
    dp.register_callback_query_handler(process_page_press, lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
    dp.register_callback_query_handler(process_bookmark_press, lambda x: x.data.isdigit())
    dp.register_callback_query_handler(process_edit_press, text='edit_bookmarks')
    dp.register_callback_query_handler(process_cancel_press, text='cancel')
    dp.register_callback_query_handler(process_delete_bookmark_press, lambda x: 'del' in x.data and x.data[:-3].isdigit())










