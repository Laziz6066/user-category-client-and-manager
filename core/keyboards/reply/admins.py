from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_reply_start_keyboard_admins():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Чаты с клиентами')
    keyboard_builder.button(text='Претензии от клиентов')
    keyboard_builder.button(text='Уведомления об обращении клиента к боту')
    keyboard_builder.adjust(2, 1)
    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
