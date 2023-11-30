from aiogram.types import Message, InputFile, FSInputFile
from aiogram.fsm.context import FSMContext
from loader import dp
from aiogram import F, Bot
from core.settings import settings
from core.utils.client_state_form import InvoiceForm
import datetime
from fpdf import FPDF
from aiogram import types
import os
from core.keyboards.reply.clients import get_payment_keyboard_clients, get_reply_start_keyboard_clients
from core.database.invoice import save_data


@dp.message(F.text == 'Создание накладной')
async def create_invoice(message: Message, state: FSMContext):
    if message.from_user.id != settings.bots.admin_id:
        await message.answer(f'{message.from_user.first_name}, начинаем Создание накладной.\r\n'
                             f'Введите описание груза.\r\n'
                             f'Например: Телевизор диагонали 43 с голосовым помощником.')
        await state.set_state(InvoiceForm.CARGO_DESCRIPTION)


@dp.message(InvoiceForm.CARGO_DESCRIPTION)
async def get_description(message: Message, state: FSMContext):
    if message.from_user.id != settings.bots.admin_id:
        await message.answer('Введите вес груза, например:\r\n5кг / 900гр / 1т ')
        await state.update_data(description=message.text)
        await state.set_state(InvoiceForm.CARGO_WEIGHT)


@dp.message(InvoiceForm.CARGO_WEIGHT)
async def get_weight(message: Message, state: FSMContext):
    if message.from_user.id != settings.bots.admin_id:
        await message.answer('Введите габариты груза. В формате X*Y*Z (в сантиметрах).'
                             '\r\nХ - длина\r\nY - ширина\r\nZ - высота')
        await state.update_data(weight=message.text)
        await state.set_state(InvoiceForm.CARGO_DIMENSIONS)


@dp.message(InvoiceForm.CARGO_DIMENSIONS)
async def get_dimensions(message: Message, state: FSMContext):
    if message.from_user.id != settings.bots.admin_id:
        await message.answer('Введите точный адрес отправки.')
        await state.update_data(dimensions=message.text)
        await state.set_state(InvoiceForm.SENDING_ADDRESS)


@dp.message(InvoiceForm.SENDING_ADDRESS)
async def get_send_address(message: Message, state: FSMContext):
    if message.from_user.id != settings.bots.admin_id:
        await message.answer('Введите точный адрес получения.')
        await state.update_data(send_address=message.text)
        await state.set_state(InvoiceForm.RECEIVING_ADDRESS)


@dp.message(InvoiceForm.RECEIVING_ADDRESS)
async def get_receiving_address(message: Message, state: FSMContext):
    if message.from_user.id != settings.bots.admin_id:
        await message.answer('Выберите способ оплаты.', reply_markup=get_payment_keyboard_clients())
        await state.update_data(receiving_address=message.text)
        await state.set_state(InvoiceForm.PAYMENT_METHOD)


# @dp.message(InvoiceForm.PAYMENT_METHOD)
# async def get_payment(message: Message, state: FSMContext):
#     if message.from_user.id != settings.bots.admin_id:
#         await message.answer("Данные записаны")
#         context_data = await state.get_data()
#         description = context_data.get('description')
#         weight = context_data.get('weight')
#         dimensions = context_data.get('dimensions')
#         send_address = context_data.get('send_address')
#         receiving_address = context_data.get('receiving_address')
#         payment = message.text
#
#         await message.answer(f"Описание груза: {description}\r\n"
#                              f"Вес груза: {weight}\r\n"
#                              f"Габариты груза: {dimensions}\r\n"
#                              f"Точный адрес отправки: {send_address}\r\n"
#                              f"Точный адрес получения: {receiving_address}\r\n"
#                              f"Способ оплаты: {payment}")
#
#         await state.clear()


async def generate_invoice_pdf(message: types.Message, data: dict, number):
    pdf = FPDF()
    pdf.add_page()

    pdf.add_font('Arial', '', 'core/utils/font/DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('Arial', '', 16)
    today = datetime.date.today()

    pdf.cell(0, 10, f'Организация: OOO CLIENTSANDMANAGERS     {today.day}.{today.month}.{today.year}',
             0, 1, 'L')
    pdf.cell(0, 10, f'Накладная   № {number}', 0, 1, 'C')

    # Add cargo description
    pdf.set_font('Arial', '', 12)
    pdf.cell(60, 10, 'Описание груза', 1, 0, 'L')
    pdf.multi_cell(100, 10, data['description'], 1, 1, '')

    # Add cargo weight
    pdf.cell(60, 10, 'Вес груза', 1, 0, 'L')
    pdf.multi_cell(100, 10, data['weight'], 1, 1, '')

    # Add cargo dimensions
    pdf.cell(60, 10, 'Габариты груза', 1, 0, 'L')
    pdf.multi_cell(100, 10, data['dimensions'], 1, 1, '')

    # Add sending address
    pdf.cell(60, 10, 'Точный адрес отправки', 1, 0, 'L')
    pdf.multi_cell(100, 10, data['send_address'], 1, 1, '')

    # Add receiving address
    pdf.cell(60, 10, 'Точный адрес получения', 1, 0, 'L')
    pdf.multi_cell(100, 10, data['receiving_address'], 1, 1, '')

    # Add payment method
    pdf.cell(60, 10, 'Способ оплаты', 1, 0, 'L')
    pdf.multi_cell(100, 10, data['payment'], 1, 1, '')

    target_directory = 'core/invoices'
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    filename = f'invoice_{message.chat.id}.pdf'
    filepath = os.path.join(target_directory, filename)
    pdf.output(filepath)

    photo = FSInputFile(path=f'core/invoices/invoice_{message.chat.id}.pdf')
    await message.reply_document(document=photo)


@dp.message(InvoiceForm.PAYMENT_METHOD)
async def get_payment(message: Message, state: FSMContext):
    if message.from_user.id != settings.bots.admin_id:
        await message.answer("Данные записаны", reply_markup=get_reply_start_keyboard_clients())
        context_data = await state.get_data()
        data = {
            'user_id': message.from_user.id,
            'description': context_data.get('description'),
            'weight': context_data.get('weight'),
            'dimensions': context_data.get('dimensions'),
            'send_address': context_data.get('send_address'),
            'receiving_address': context_data.get('receiving_address'),
            'payment': message.text
        }
        id_inv = await save_data(data['user_id'], data['description'], data['weight'], data['dimensions'],
                                 data['send_address'],data['receiving_address'], data['payment'])

        await state.clear()

        await generate_invoice_pdf(message, data, id_inv)
