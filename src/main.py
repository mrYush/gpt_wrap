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

from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from scrip_utils import get_logger, get_kwargs
from settings import TELEGRAM_TOKEN
from telegram_utils import start, help_command, gpt_answer, make_picture, choose_context, button, get_user_info


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
    application.add_handler(
        CommandHandler("context", choose_context)
    )
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(
        CommandHandler("usr", get_user_info)
    )
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    FILE_NAME = Path(__file__)
    default_config_path = (Path(__file__).parent /
                           f'{Path(__file__).stem}_config.yml')
    kwargs = get_kwargs(default_config_path=default_config_path).parse_args()
    LOGGER = get_logger(logger_name=FILE_NAME.stem, path=FILE_NAME.parent,
                        level=kwargs.logger_level)
    main()
