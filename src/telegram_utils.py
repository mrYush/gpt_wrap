"""Module for telegram handlers"""
import re

from telegram import Update, ForceReply
from telegram.ext import ContextTypes

from src.gpt_utils import get_answer, get_gen_pic_url
from src.main import LOGGER, PIC_COMMAND


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def gpt_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    user = update.effective_user
    LOGGER.info(f"new_request: {user.id}; {user.mention_html()}; {update.message.text}")
    await update.message.reply_text(get_answer(update.message.text))


async def make_picture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the image generated on request"""
    user = update.effective_user
    LOGGER.info(f"new_request: {user.id}; {user.mention_html()}; {update.message.text}")
    pic_url = get_gen_pic_url(text_description=re.sub(f"/{PIC_COMMAND}", "", update.message.text))
    print(pic_url)
    chat_id = update.effective_chat.id
    await context.bot.send_photo(chat_id=chat_id, photo=pic_url)
