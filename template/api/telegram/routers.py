import logging

from aiogram import Router
from aiogram.filters import (
    CommandStart,
)
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from template.api.telegram.dialogs.main import MainStateGroup

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart())
async def start_handler(_: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(MainStateGroup.main, mode=StartMode.RESET_STACK)
