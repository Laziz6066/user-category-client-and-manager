from aiogram.filters import CommandStart
from aiogram.types import Message
from loader import dp
from core.keyboards.reply.clients import get_reply_start_keyboard_clients
from core.keyboards.reply.admins import get_reply_start_keyboard_admins
from core.settings import settings


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.from_user.id == settings.bots.admin_id:
        await message.answer(f"Добро пожаловать!", reply_markup=get_reply_start_keyboard_admins())
    else:
        await message.answer(f"Добро пожаловать!", reply_markup=get_reply_start_keyboard_clients())


