"""Module for telegram handlers"""
import logging
import re

from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from db_utils.scheme import check_user, set_current_context
from src.gpt_utils import get_answer, get_gen_pic_url

LOGGER = logging.getLogger()
PIC_COMMAND = "pic"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    check_user(user=user , return_mongo_user=False)
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user = update.effective_user
    check_user(user=user)
    msg = (
        f"Hello, {user.name}!\nSend me a message and I answer you.\n"
        f"Send /pic + description and I'll create an image.\n"
        f"Without context, I can respond rapidly (4-5 seconds).\n"
        f"If You want to use context send me "
        f"/context and follow the instructions."
    )
    await update.message.reply_text(msg)


async def gpt_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    user = update.effective_user
    text = get_answer(text=update.message.text)

    await update.message.reply_text(text)


async def make_picture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the image generated on request"""
    user = update.effective_user
    LOGGER.info(f"new_request: {user.id}; {user.mention_html()}; {update.message.text}")
    pic_url = get_gen_pic_url(text_description=re.sub(f"/{PIC_COMMAND}", "", update.message.text))
    print(pic_url)
    chat_id = update.effective_chat.id
    await context.bot.send_photo(chat_id=chat_id, photo=pic_url)


async def choose_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wo_context = InlineKeyboardButton(text='без контекста', callback_data="context_0")
    last_10 = InlineKeyboardButton(text='последние 10 сообщений', callback_data="context_10")
    urlkb = InlineKeyboardMarkup(inline_keyboard=[[wo_context, last_10]])
    await update.message.reply_text("вот", reply_markup=urlkb)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    user = update.effective_user
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    mes = f"Selected option: {query.data}, {type(query.data)}, User is {user.id}, {context.chat_data}"
    set_current_context(user=user, context_name=query.data)
    await query.answer(text=mes)
    # await query.(text=f"Selected option: {query.data}, User is {user.id}")
    # await context.bot.send_message()
    # await query.edit_message_text(text=f"Selected option: {query.data}, User is {user.id}")


async def get_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """return user_info"""
    user = update.effective_user
    # print(user.id, user.full_name)
    await update.message.reply_text(text=f"User is {user.id}")
