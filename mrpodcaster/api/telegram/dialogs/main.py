import logging

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Start
from aiogram_dialog.widgets.text import Const, Format

from mrpodcaster.api.telegram.dialogs.view_podcast import PodcastViewSG
from mrpodcaster.api.telegram.utils import USER_NAME

logger = logging.getLogger(__name__)


class MainSG(StatesGroup):
    main = State()
    help = State()
    about = State()


async def getter(
    dialog_manager: DialogManager,
    **_,
):
    return {
        "username": dialog_manager.middleware_data[USER_NAME].username,
    }


dialog = Dialog(
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
                state=MainSG.help,
            ),
            Start(
                Const("Choose podcasts!"),
                id="choose_podcasts" "",
                state=PodcastViewSG.level,
            ),
            SwitchTo(Const("Authors"), id="authors", state=MainSG.about),
            width=1,
        ),
        state=MainSG.main,
        parse_mode="Markdown",
        getter=getter,
    ),
    Window(
        Format(
            "This is how Mr. Podcastov helps you {username}\n"
            "\t1) There are 3 levels of difficulty\n"
            "\t2) Choose your level and progress throughout the week\n"
            "\t3) At the end of the week Mr. Podcastov will match you with a random partner who listened to the same podcast as you and you can start a discussion!\n"
            "\t4) Monitor your progress\n"
            "\t5) Mr. Podcastov will add new podcasts next week!\n"
        ),
        SwitchTo(Const("Back"), id="back", state=MainSG.main),
        state=MainSG.help,
        parse_mode="Markdown",
        getter=getter,
    ),
    Window(
        Format("*About the authors*"),
        SwitchTo(Const("Back"), id="back", state=MainSG.main),
        state=MainSG.about,
    ),
)
