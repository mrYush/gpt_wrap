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
from pathlib import Path

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from scrip_utils import get_logger
from settings import TELEGRAM_TOKEN
from src.telegram_utils import start, help_command, gpt_answer, make_picture

file_name = Path(__file__)
LOGGER = get_logger(logger_name=file_name.stem, path=file_name.parent)
PIC_COMMAND = "pic"


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
