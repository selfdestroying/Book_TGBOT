from aiogram import Dispatcher, types

from lexicon.lexicon_ru import LEXICON


# Settings Menu button
async def set_main_menu(dp: Dispatcher):
    main_menu_commands = [
        types.BotCommand(command='/beginning', description=LEXICON['/beginning']),
        types.BotCommand(command='/continue', description=LEXICON['/continue']),
        types.BotCommand(command='/bookmarks', description=LEXICON['/bookmarks']),
        types.BotCommand(command='/help', description=LEXICON['/help'][:64])]
    await dp.bot.set_my_commands(main_menu_commands)