import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import load_config
from handlers.other_handlers import register_echo_handler
from handlers.user_handlers import register_user_handlers
from keyboards.main_menu import set_main_menu
# Initialize logger
logger = logging.getLogger(__name__)


# All handlers registration function
def register_all_handlers(dp: Dispatcher) -> None:
    register_user_handlers(dp)
    register_echo_handler(dp)


# Configure and start main thread
async def main():
    # Logging configuration
    logging.basicConfig(level=logging.INFO, format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
                                                   u'[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Bot started!')

    # Load bot configuration
    config = load_config('.env')  # Path to .env file

    # Initialize bot and dispatcher
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot=bot)

    # Set bot main menu
    await set_main_menu(dp)

    # Register all handlers
    register_all_handlers(dp)

    # Start polling
    try:
        await dp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
