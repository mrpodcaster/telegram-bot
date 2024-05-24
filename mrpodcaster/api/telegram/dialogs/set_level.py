import logging
import operator

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Format

from mrpodcaster.authentication.models import DifficultyLevel

logger = logging.getLogger(__name__)


class SetLevelStateGroup(StatesGroup):
    main = State()


async def level_select_getter(dialog_manager: DialogManager, **_):
    return {
        "current_level": dialog_manager.current_context().dialog_data.get(
            "current_level", "NONE"
        ),
        "levels": DifficultyLevel.choices,
    }


# async def set_level(
#     query: CallbackQuery, select: Select, dialog_manager: DialogManager, level: str
# ):
#     USER_DATA["selected_difficulty_level"] = level
#     await query.answer(f"Your level set to: {level}")
#     print(f"Your current level is: {level}!")
#     await dialog_manager.done()


async def set_level(
    query: CallbackQuery, select: Select, dialog_manager: DialogManager, level: str
):
    # Update the difficulty level in the current context
    dialog_manager.current_context().dialog_data["current_level"] = level

    await query.answer(f"Your level set to: {level}")
    # Now fetch the updated level from the current context for the message
    updated_level = dialog_manager.current_context().dialog_data["current_level"]
    print(f"Your current level is: {updated_level}!")
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
