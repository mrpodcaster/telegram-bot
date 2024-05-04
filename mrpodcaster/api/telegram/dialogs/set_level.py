import logging
import operator

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Format

from mrpodcaster.api.telegram.utils import USER_NAME
from mrpodcaster.authentication.models import TelegramUser, DifficultyLevel

logger = logging.getLogger(__name__)


class SetLevelStateGroup(StatesGroup):
    main = State()


async def level_select_getter(dialog_manager: DialogManager, **_):
    user: TelegramUser = dialog_manager.middleware_data[USER_NAME]
    return {"current_level": user.level, "levels": DifficultyLevel.choices}


async def set_level(
    query: CallbackQuery, select: Select, dialog_manager: DialogManager, level: str
):
    await query.answer(f"Your level set to: {level}")
    user: TelegramUser = dialog_manager.middleware_data[USER_NAME]
    user.level = level
    await user.asave()
    await dialog_manager.done()


set_level_window = Dialog(
    Window(
        Format("Your current level is: {current_level}\n" "Choose your new level"),
        Select(
            Format("{item[0]}"),
            items="levels",
            item_id_getter=operator.itemgetter(0),
            id="level_select",
            on_click=set_level,
        ),
        state=SetLevelStateGroup.main,
        getter=level_select_getter,
    ),
)
