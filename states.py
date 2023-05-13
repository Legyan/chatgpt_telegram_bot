from aiogram.fsm.state import State, StatesGroup


class Gen(StatesGroup):
    text_prompt = State()
    img_prompt = State()
