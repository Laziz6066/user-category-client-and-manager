import asyncio
from aiogram import Bot
from aiogram.enums import ParseMode
import logging
from core.handlers.start import command_start_handler
from core.settings import settings
from loader import dp
from core.utils.commands import set_commands
from aiogram import F
from core.handlers.clients.creating_invoice import create_invoice
from core.handlers.clients.creating_claim import create_claim


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен')


# dp.startup.register(start_bot)
# dp.shutdown.register(stop_bot)
dp.message.register(command_start_handler, F.text == 'start')
dp.message.register(create_invoice, F.text == 'Создание накладной')
dp.message.register(create_claim, F.text == 'Регистрация претензии')


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = Bot(settings.bots.bot_token, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())