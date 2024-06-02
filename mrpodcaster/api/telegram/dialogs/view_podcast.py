import operator
from typing import Callable

import loguru
from aiogram import F
from aiogram.enums import ContentType
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, FSInputFile
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Select, Cancel, SwitchTo, Button, Group
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi, Case
from django.db.models import Exists, OuterRef

from mrpodcaster.api.models import DifficultyLevel, Podcast, PodcastView
from mrpodcaster.api.telegram.utils import USER_NAME
from mrpodcaster.authentication.models import TelegramUser


class PodcastViewSG(StatesGroup):
    level = State()
    podcast = State()

    view = State()


async def select_level(
        query: CallbackQuery, select: Select, dialog_manager: DialogManager, level: str
):
    await query.answer(f"Level {level} selected!")
    dialog_manager.dialog_data.clear()
    dialog_manager.dialog_data["level"] = level
    await dialog_manager.switch_to(PodcastViewSG.podcast)


async def podcasts_getter(dialog_manager: DialogManager, **_) -> dict:
    if 'podcasts' in dialog_manager.dialog_data:
        return dialog_manager.dialog_data['podcasts'][dialog_manager.dialog_data['current_index']]

    level = dialog_manager.dialog_data['level']
    podcasts = [podcast async for podcast in Podcast.objects.filter(
        difficulty=level, archived=False
    ).annotate(
        viewed=Exists(PodcastView.objects.filter(podcast=OuterRef('pk')))
    ).values("id", "title", "description", "viewed", "file")]

    if len(podcasts) == 0:
        dialog_manager.dialog_data['podcasts'] = []
        return {}
    loguru.logger.error(podcasts)
    dialog_manager.dialog_data['current_index'] = 0
    dialog_manager.dialog_data['podcasts'] = podcasts
    dialog_manager.dialog_data['left'] = 0
    dialog_manager.dialog_data['right'] = len(podcasts) - 1

    return dialog_manager.dialog_data['podcasts'][dialog_manager.dialog_data['current_index']]


def scroller(operation: Callable[[int, int], int]) -> OnClick:
    async def on_click(query: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
        current_index = dialog_manager.dialog_data["current_index"]
        dialog_manager.dialog_data["current_index"] = operation(current_index, 1)
        dialog_manager.dialog_data['podcast'] = dialog_manager.dialog_data['podcasts'][current_index]

    return on_click


async def choose_podcast(query: CallbackQuery, button: Button, dialog_manager: DialogManager):
    user: TelegramUser = dialog_manager.middleware_data[USER_NAME]
    podcast = dialog_manager.dialog_data['podcasts'][dialog_manager.dialog_data['current_index']]
    loguru.logger.error(
        f"User {user.username} have chosen a podcast {podcast}")
    _, created = await PodcastView.objects.aget_or_create(
        podcast_id=podcast['id'],
        user=user
    )
    if not created:
        await query.answer("Warning: You've listened for that podcast already")

    await dialog_manager.switch_to(PodcastViewSG.view)


async def podcast_view_getter(dialog_manager: DialogManager, **_) -> dict:
    podcast = dialog_manager.dialog_data['podcasts'][dialog_manager.dialog_data['current_index']]
    file = (await Podcast.objects.filter(id=podcast['id']).aget()).file
    loguru.logger.info(file.url)

    return {
        **podcast,
        'file': MediaAttachment(ContentType.AUDIO, path=file.path, use_pipe=True),
    }


dialog = Dialog(
    Window(
        Const("Select level!"),
        Select(
            Format("{item[0]}"),
            items=DifficultyLevel.choices,
            item_id_getter=operator.itemgetter(0),
            id="level_select",
            on_click=select_level,
        ),
        Cancel(Const("Back"), id="back"),
        state=PodcastViewSG.level,
    ),
    Window(
        Case(
            {
                0: Const("No podcasts on this level :^("),
                ...: Multi(
                    Const("Select podcast!"),
                    Const("✅", when=F["viewed"]),
                    Format(
                        "*{title}*\n\n{description}",
                    ))
            },

            selector=F['dialog_data']['podcasts'].len()
        ),
        Group(
            Button(Const("<"), id="scroll_left", on_click=scroller(operation=operator.sub),
                   when=F['dialog_data']['left'].__lt__(F['dialog_data']['current_index'])),
            Button(Format("Choose me!"), id="choose", on_click=choose_podcast),
            Button(Const(">"), id="scroll_right", on_click=scroller(operation=operator.add),
                   when=F['dialog_data']['right'].__gt__(F['dialog_data']['current_index'])),
            width=3,
            when=F['dialog_data']['podcasts'].len() > 0
        ),
        SwitchTo(Const("Back"), id="back", state=PodcastViewSG.level),
        getter=podcasts_getter,
        state=PodcastViewSG.podcast,
        parse_mode="Markdown",
    ),
    Window(
        Format("*{title}*\n\n{description}", ),
        DynamicMedia("file"),
        SwitchTo(Const("Back"), id="back", state=PodcastViewSG.podcast),
        getter=podcast_view_getter,
        state=PodcastViewSG.view,
        parse_mode="Markdown"
    )
)
