from aiogram.fsm.state import StatesGroup, State


class InvoiceForm(StatesGroup):
    CARGO_DESCRIPTION = State()
    CARGO_WEIGHT = State()
    CARGO_DIMENSIONS = State()
    SENDING_ADDRESS = State()
    RECEIVING_ADDRESS = State()
    PAYMENT_METHOD = State()


class ClaimForm(StatesGroup):
    INVOICE_NUMBER = State()
    EMAIL = State()
    SITUATION_DESCRIPTION = State()
    REQUIRED_AMOUNT = State()
    PHOTOS_SCANS = State()