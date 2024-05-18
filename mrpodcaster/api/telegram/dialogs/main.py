import logging
from typing import TypedDict

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Start
from aiogram_dialog.widgets.text import Const, Format

from mrpodcaster.api.telegram.dialogs.set_level import SetLevelStateGroup
from mrpodcaster.api.telegram.utils import USER_NAME

logger = logging.getLogger(__name__)


class MainStateGroup(StatesGroup):
    main = State()
    help = State()
    about = State()


class MainWindowGetterData(TypedDict):
    username: str


async def getter(
    dialog_manager: DialogManager,
    **_,
):
    return MainWindowGetterData(
        username=dialog_manager.middleware_data[USER_NAME].username,
    )


main_window = Dialog(
    Window(
        Format(
            "Hello, {username}!\n"
            "I am Mr. Podcastov. I have something interesting for you to listen to and share with others\n\n"
            "Are you ready to start?"
        ),
        Group(
            SwitchTo(
                Const("How do you work Mr. Podcastov?"),
                id="help",
                state=MainStateGroup.help,
            ),
            Start(
                Const("I want to choose my level"),
                id="choose_level",
                state=SetLevelStateGroup.main,
            ),
            SwitchTo(Const("Authors"), id="authors", state=MainStateGroup.about),
            width=1,
        ),
        state=MainStateGroup.main,
        parse_mode="Markdown",
        getter=getter,
    ),
    Window(
        Format(
            "This is how Mr. Podcastov helps you *{username}*\n"
            "\t☑️ There are 3 levels of difficulty\n"
            "\t☑️ Choose your level and progress throughout the week\n"
            "\t☑️ At the end of the week Mr. Podcastov will match you with a random partner who listened to the same podcast as you and you can start a discussion!\n"
            "\t☑️ Monitor your progress\n"
            "\t☑️ Mr. Podcastov will add new podcasts next week!\n"
        ),
        SwitchTo(Const("Back"), id="back", state=MainStateGroup.main),
        state=MainStateGroup.help,
        parse_mode="Markdown",
        getter=getter,
    ),
    Window(
        Format("*About the authors*"),
        SwitchTo(Const("Back"), id="back", state=MainStateGroup.main),
        state=MainStateGroup.about,
    ),
)
