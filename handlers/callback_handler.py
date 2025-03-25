from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database import Database
from utils import ButtonManager, humanbytes
import config
import logging
from datetime import datetime
import pytz

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database and button manager
db = Database()
button_manager = ButtonManager()

@Client.on_callback_query(filters.regex(r"^home"))
async def home_callback(client: Client, callback_query: CallbackQuery):
    try:
        await callback_query.message.edit_text(
            config.Messages.START_TEXT.format(
                bot_name=config.BOT_NAME,
                user_mention=callback_query.from_user.mention
            ),
            reply_markup=button_manager.start_button()
        )
    except Exception as e:
        logger.error(f"Error in home callback: {str(e)}")
        await callback_query.answer("❌ An error occurred", show_alert=True)

@Client.on_callback_query(filters.regex(r"^help"))
async def help_callback(client: Client, callback_query: CallbackQuery):
    try:
        await callback_query.message.edit_text(
            config.Messages.HELP_TEXT,
            reply_markup=button_manager.help_button()
        )
    except Exception as e:
        logger.error(f"Error in help callback: {str(e)}")
        await callback_query.answer("❌ An error occurred", show_alert=True)

@Client.on_callback_query(filters.regex(r"^about"))
async def about_callback(client: Client, callback_query: CallbackQuery):
    try:
        await callback_query.message.edit_text(
            config.Messages.ABOUT_TEXT.format(
                bot_name=config.BOT_NAME,
                version=config.BOT_VERSION
            ),
            reply_markup=button_manager.about_button()
        )
    except Exception as e:
        logger.error(f"Error in about callback: {str(e)}")
        await callback_query.answer("❌ An error occurred", show_alert=True)

@Client.on_callback_query(filters.regex(r"^download_"))
async def download_callback(client: Client, callback_query: CallbackQuery):
    try:
        # Extract file UUID from callback data
        file_uuid = callback_query.data.split("_")[1]
        
        # Get file data from database
        file_data = await db.get_file(file_uuid)
        if not file_data:
            await callback_query.answer("File not found or expired!", show_alert=True)
            return

        # Check if user is banned
        if await db.is_user_banned(callback_query.from_user.id):
            await callback_query.answer("You are banned from using this bot!", show_alert=True)
            return

        # Send status message
        status_msg = await callback_query.message.reply_text(
            "🔄 **Processing Download**\n\n⏳ Please wait..."
        )

        try:
            # Copy file to user
            await client.copy_message
