from typing import List, Union
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import config
import logging

logger = logging.getLogger(__name__)

class ButtonManager:
    def __init__(self):
        self.force_sub_channel = config.FORCE_SUB_CHANNEL
        self.db_channel = config.DB_CHANNEL_ID

    async def check_force_sub(self, client, user_id: int) -> bool:
        try:
            member = await client.get_chat_member(self.force_sub_channel, user_id)
            if member.status in ["left", "kicked"]:
                return False
            return True
        except Exception as e:
            logger.error(f"Force sub check error: {str(e)}")
            return False

    async def show_start(self, client, callback_query: CallbackQuery):
        try:
            await callback_query.message.edit_text(
                config.Messages.START_TEXT.format(
                    bot_name=config.BOT_NAME,
                    user_mention=callback_query.from_user.mention
                ),
                reply_markup=self.start_button()
            )
        except Exception as e:
            logger.error(f"Show start error: {str(e)}")

    async def show_help(self, client, callback_query: CallbackQuery):
        try:
            await callback_query.message.edit_text(
                config.Messages.HELP_TEXT,
                reply_markup=self.help_button()
            )
        except Exception as e:
            logger.error(f"Show help error: {str(e)}")

    async def show_about(self, client, callback_query: CallbackQuery):
        try:
            await callback_query.message.edit_text(
                config.Messages.ABOUT_TEXT.format(
                    bot_name=config.BOT_NAME,
                    version=config.BOT_VERSION
                ),
                reply_markup=self.about_button()
            )
        except Exception as e:
            logger.error(f"Show about error: {str(e)}")

    def force_sub_button(self) -> InlineKeyboardMarkup:
        buttons = [[
            InlineKeyboardButton(
                "Join Channel 🔔",
                url=config.CHANNEL_LINK
            )
        ]]
        return InlineKeyboardMarkup(buttons)

    def start_button(self) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton("Help 📜", callback_data="help"),
                InlineKeyboardButton("About ℹ️", callback_data="about")
            ],
            [
                InlineKeyboardButton("Channel 📢", url=config.CHANNEL_LINK),
                InlineKeyboardButton("Developer 👨‍💻", url=config.DEVELOPER_LINK)
            ]
        ]
        return InlineKeyboardMarkup(buttons)

    def help_button(self) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton("Home 🏠", callback_data="home"),
                InlineKeyboardButton("About ℹ️", callback_data="about")
            ],
            [
                InlineKeyboardButton("Channel 📢", url=config.CHANNEL_LINK)
            ]
        ]
        return InlineKeyboardMarkup(buttons)

    def about_button(self) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton("Home 🏠", callback_data="home"),
                InlineKeyboardButton("Help 📜", callback_data="help")
            ],
            [
                InlineKeyboardButton("Channel 📢", url=config.CHANNEL_LINK)
            ]
        ]
        return InlineKeyboardMarkup(buttons)

    def file_button(self, file_uuid: str) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton("Download 📥", callback_data=f"download_{file_uuid}"),
                InlineKeyboardButton("Share Link 🔗", callback_data=f"share_{file_uuid}")
            ],
            [
                InlineKeyboardButton("Channel 📢", url=config.CHANNEL_LINK)
            ]
        ]
        return InlineKeyboardMarkup(buttons)

    def batch_button(self, batch_uuid: str) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton("Download All 📥", callback_data=f"dlbatch_{batch_uuid}"),
                InlineKeyboardButton("Share Link 🔗", callback_data=f"share_batch_{batch_uuid}")
            ],
            [
                InlineKeyboardButton("Channel 📢", url=config.CHANNEL_LINK)
            ]
        ]
        return InlineKeyboardMarkup(buttons)
