from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Dialog, Window


class PodcastSG(StatesGroup):
    main = State()


dialog = Dialog(
    Window(
    state=PodcastSG.main
    )

)
