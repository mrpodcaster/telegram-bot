from typing import TypedDict

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Start
from aiogram_dialog.widgets.text import Const, Format

from mrpodcaster.api.telegram.dialogs.set_level import (
    SetLevelStateGroup,
)
from mrpodcaster.api.telegram.utils import USER_NAME
import logging
from aiogram_dialog.widgets.kbd import Button
from aiogram.types import CallbackQuery


logger = logging.getLogger(__name__)


class MainStateGroup(StatesGroup):
    main = State()
    help = State()
    about = State()
    podcasts = State()
    selected_podcast = State()


class PodcastsListStateGroup(StatesGroup):
    listing = State()


class MainWindowGetterData(TypedDict):
    username: str


id_to_title_map = {}
userLevels = {}
podcasts_by_level = {
    "easy": ["Why r u gae", "Other Podcast 1", "Another 1"],
    "medium": ["Who says I'm gae", "Other Podcast 2", "Another 2"],
    "challenging": ["...", "Other Podcast 3", "Another 3"],
}


async def getter(
    dialog_manager: DialogManager,
    **_,
):
    return MainWindowGetterData(
        username=dialog_manager.middleware_data[USER_NAME].username,
    )


async def get_podcasts(dialog_manager: DialogManager, **_):
    user_level = (
        dialog_manager.current_context().dialog_data.get("current_level", "easy"),
    )
    available_podcasts = podcasts_by_level.get(user_level, [])

    # Create podcast buttons for the available podcasts
    buttons = await create_podcast_buttons(available_podcasts)

    return {"podcasts": available_podcasts, "buttons": buttons}


def sanitize_id(title: str) -> str:
    """Convert a title to a valid ID by removing problematic characters."""
    return title.translate(str.maketrans("", "", " '?,.!/()\"")).lower()


async def on_podcast_click(
    callback_query: CallbackQuery, button: Button, manager: DialogManager
):
    _, sanitized_podcast_id = callback_query.data.split("_", 2)[:]
    original_podcast_title = id_to_title_map.get(
        sanitized_podcast_id, "Unknown Podcast"
    )
    manager.current_context().dialog_data["selected_podcast"] = original_podcast_title
    await manager.switch_to(MainStateGroup.selected_podcast)


async def create_podcast_buttons(podcasts):
    buttons = []
    for podcast in podcasts:
        sanitized_id = sanitize_id(podcast)
        id_to_title_map[sanitized_id] = podcast
        buttons.append(
            Button(
                Const(podcast),
                id=f"podcast_{sanitized_id}",
                on_click=on_podcast_click,
            )
        )
    return buttons


# NOT ASYNC
def make_podcast_buttons(podcasts):
    buttons = []
    for podcast in podcasts:
        sanitized_id = sanitize_id(podcast)
        id_to_title_map[sanitized_id] = podcast
        buttons.append(
            Button(
                Const(podcast),
                id=f"podcast_{sanitized_id}",
                on_click=on_podcast_click,
            )
        )
    return buttons


async def get_the_podcast(dialog_manager: DialogManager, **kwargs):
    data = MainWindowGetterData(
        username=dialog_manager.middleware_data[USER_NAME].username,
        podcast=dialog_manager.current_context().dialog_data.get(
            "podcast", "No podcast selected"
        ),
    )
    return data


podcasts_window = Window(
    Const("Podcasts for your level:"),
    Group(
        #! BUG IS HERE, NEED TO REPLACE THE HARDCODED LIST ON THE ONE FROM --- async get_podcasts()
        *make_podcast_buttons(["Why r u gae", "Who says I'm gae", "..."]),
        id="podcasts_group",
        width=1,
    ),
    SwitchTo(Const("Back"), id="back", state=MainStateGroup.main),
    state=MainStateGroup.podcasts,
    getter=get_podcasts,
    parse_mode="Markdown",
)


async def selected_podcast_getter(dialog_manager: DialogManager, **_):
    return dialog_manager.current_context().dialog_data


selected_podcast_window = Window(
    Format("You selected podcast: {selected_podcast}"),
    SwitchTo(Const("Back"), id="back", state=MainStateGroup.podcasts),
    state=MainStateGroup.selected_podcast,
    getter=selected_podcast_getter,
    parse_mode="Markdown",
)

main_window = Dialog(
    podcasts_window,
    selected_podcast_window,
    Window(
        Format(
            "Hello, {username}!\n"
            "I am Mr. Podcastov. I have something interesting for you to listen to and share with others\n\n"
            "Are you ready to start?"
        ),
        Group(
            SwitchTo(
                Const("List Podcasts"),
                id="list_podcasts",
                state=MainStateGroup.podcasts,
            ),
            width=1,
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
            "This is how Mr. Podcastov helps you {username}\n"
            "\t1) There are 3 levels of difficulty\n"
            "\t2) Choose your level and progress throughout the week\n"
            "\t3) At the end of the week Mr. Podcastov will match you with a random partner who listened to the same podcast as you and you can start a discussion!\n"
            "\t4) Monitor your progress\n"
            "\t5) Mr. Podcastov will add new podcasts next week!\n"
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
