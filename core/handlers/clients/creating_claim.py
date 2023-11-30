from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from loader import dp
from aiogram import F, Bot
from core.settings import settings
from core.utils.client_state_form import ClaimForm
from core.database.claim import save_data


@dp.message(F.text == 'Регистрация претензии')
async def create_claim(message: Message, state: FSMContext):
    if message.from_user.id != settings.bots.admin_id:
        await message.answer(f'{message.from_user.first_name}, начинаем Создание претензии.\r\n'
                             f'Введите номер накладной.')
        await state.set_state(ClaimForm.INVOICE_NUMBER)


@dp.message(ClaimForm.INVOICE_NUMBER)
async def get_invoice_number(message: Message, state: FSMContext):
    if message.from_user.id != settings.bots.admin_id:
        await message.answer('Введите e-mail для ответа на претензию.')
        await state.update_data(invoice_number=message.text)
        await state.set_state(ClaimForm.EMAIL)


@dp.message(ClaimForm.EMAIL)
async def get_e_mail(message: Message, state: FSMContext):
    if message.from_user.id != settings.bots.admin_id:
        await message.answer('Введите описание ситуации.')
        await state.update_data(e_mail=message.text)
        await state.set_state(ClaimForm.SITUATION_DESCRIPTION)


@dp.message(ClaimForm.SITUATION_DESCRIPTION)
async def get_description(message: Message, state: FSMContext):
    if message.from_user.id != settings.bots.admin_id:
        await message.answer('Введите требуемую сумму.')
        await state.update_data(description=message.text)
        await state.set_state(ClaimForm.REQUIRED_AMOUNT)


@dp.message(ClaimForm.REQUIRED_AMOUNT)
async def get_amount(message: Message, state: FSMContext):
    if message.from_user.id != settings.bots.admin_id:
        await message.answer('Отправьте фото/сканы.')
        await state.update_data(amount=message.text)
        await state.set_state(ClaimForm.PHOTOS_SCANS)


@dp.message(ClaimForm.PHOTOS_SCANS)
async def get_photo_scan(message: Message, state: FSMContext, bot: Bot):
    if message.from_user.id != settings.bots.admin_id:
        await message.answer("Данные записаны")
        context_data = await state.get_data()
        invoice_number = context_data.get('invoice_number')
        e_mail = context_data.get('e_mail')
        description = context_data.get('description')
        amount = context_data.get('amount')
        photo_scan = message.text

        await bot.send_message(chat_id=settings.bots.admin_id, text=f"Номер накладной: {invoice_number}\r\n"
                             f"E-mail для ответа на претензию: {e_mail}\r\n"
                             f"Описание ситуации: {description}\r\n"
                             f"Требуемая сумма: {amount}\r\n"
                             f"Фото/сканы: {photo_scan}")

        await save_data(invoice_number, e_mail, description, amount, photo_scan)
        await state.clear()

