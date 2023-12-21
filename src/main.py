"""
This module contains the main function to run the bot.
"""
from pathlib import Path

from telegram.ext import Application, CommandHandler, MessageHandler, \
    filters, CallbackQueryHandler

from db_utils.db_initiate import init_db
from scrip_utils import get_logger, get_kwargs
from settings import TELEGRAM_TOKEN
from telegram_utils import start, help_command, gpt_answer, make_picture, \
    button, get_user_info, show_context, SHOW_CONTEXT, \
    PIC_COMMAND, set_system_prompt


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
        CommandHandler(PIC_COMMAND, make_picture)
    )
    application.add_handler(
        CommandHandler(SHOW_CONTEXT, show_context)
    )
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(
        CommandHandler("usr", get_user_info)
    )
    application.add_handler(
        CommandHandler("set_system_prompt", set_system_prompt)
    )
    application.run_polling()


if __name__ == "__main__":
    FILE_NAME = Path(__file__)
    default_config_path = (Path(__file__).parent /
                           f'{Path(__file__).stem}_config.yml')
    kwargs = get_kwargs(default_config_path=default_config_path).parse_args()
    LOGGER = get_logger(logger_name=FILE_NAME.stem, path=FILE_NAME.parent,
                        level=kwargs.logger_level)
    init_db()
    main()
