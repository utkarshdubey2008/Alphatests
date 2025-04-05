from pyrogram import Client, filters
from pyrogram.types import Message
from utils import is_admin

@Client.on_message(filters.command("auto_del"))
async def auto_delete_command(client: Client, message: Message):
    if not is_admin(message):
        await message.reply_text("⚠️ You are not authorized to use this command!")
        return

    await message.reply_text(
        "**⚙️ Auto Delete Time Configuration Moved**\n\n"
        "The auto-delete feature has been shifted to the `config.py` file.\n"
        "Please open your `config.py` and set the value for `AUTO_DELETE_TIME` there.\n\n"
        "**Example:**\n"
        "`AUTO_DELETE_TIME = 30  # in minutes`\n\n"
        "Restart the bot after updating the configuration to apply changes."
    )
