"""Module for temporary stub when moving from one bot to another"""
from datetime import datetime
from pathlib import Path

from telegram.ext import Application, MessageHandler

from scrip_utils import get_kwargs, get_yaml_config, get_logger
from settings import TELEGRAM_TOKEN


async def start_stub(update, context):
    """Stub for start command"""
    now = datetime.now()
    cur_dt = now.strftime("%d-%m-%Y %H:%M:%S")
    with open('stub.txt', 'a') as file:
        file.write(f"{cur_dt} {update.effective_user.id}\n")
    await update.message.reply_text(
        f"Я переехал в нового бота @{new_bot}.\n"
        f"Пиши туда и я с радостью отвечу!"
    )


if __name__ == "__main__":
    FILE_NAME = Path(__file__)
    default_config_path = (Path(__file__).parent /
                           f'{Path(__file__).stem}_config.yaml')
    kwargs = get_kwargs(default_config_path=default_config_path).parse_args()
    config = get_yaml_config(path=kwargs.config_path)
    new_bot = config.get('NEW_BOT')
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters=None, callback=start_stub))
    LOGGER = get_logger(logger_name=FILE_NAME.stem, path=FILE_NAME.parent,
                        level=kwargs.logger_level)
    LOGGER.info(f"Start bot {FILE_NAME.stem}")
    application.run_polling()
