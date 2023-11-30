from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_reply_start_keyboard_clients():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Создание накладной')
    keyboard_builder.button(text='Регистрация претензии')
    keyboard_builder.button(text='Вызов менеджера поддержки в чат')
    keyboard_builder.adjust(2, 1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_payment_keyboard_clients():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Наличными')
    keyboard_builder.button(text='Безналичными')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)