from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const


class PodcastStateGroup(StatesGroup):
    main = State()


dialog = Dialog(
    Window(
        Const("There shall be available podcasts"),
        Cancel(Const("Back")),
        state=PodcastStateGroup.main
    )
)
