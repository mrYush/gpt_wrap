#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import re
from pathlib import Path

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, \
    MessageHandler, filters

from gpt_utils import get_answer, get_gen_pic_url
from scrip_utils import get_logger
from settings import TELEGRAM_TOKEN

file_name = Path(__file__)
LOGGER = get_logger(logger_name=file_name.stem, path=file_name.parent)
PIC_COMMAND = "pic"

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


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_answer)
    )
    application.add_handler(
        CommandHandler("pic", make_picture)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
