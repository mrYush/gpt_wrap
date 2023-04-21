"""Module for telegram handlers"""
import logging
import re
from datetime import datetime

from openai import InvalidRequestError
from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from db_utils.scheme import check_user, set_current_context, ConversationCollection, get_last_n_message, \
    get_last_n_message_tokens
from gpt_utils import get_answer, get_gen_pic_url

LOGGER = logging.getLogger()
PIC_COMMAND = "pic"
SHOW_CONTEXT = 'show_context'


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


async def gpt_answer(update: Update,
                     context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    user = update.effective_user
    mongo_user = check_user(user=user, return_mongo_user=True)
    current_context = mongo_user.current_context
    request = update.message.text
    ConversationCollection(
        telegram_id=user.id,
        context_id=mongo_user.current_context,
        role='user',
        content=request,
        timestamp=datetime.now().timestamp()
    ).save()
    if current_context is None:
        kwargs = {'prompt': request}
    else:
        # kwargs = {'messages': get_last_n_message(user_id=user.id, count=10)}
        kwargs = {'messages': get_last_n_message_tokens(user_id=user.id, system_prompt=None)}
    try:
        response = get_answer(**kwargs)
        ConversationCollection(
            telegram_id=user.id,
            context_id=mongo_user.current_context,
            role='assistant',
            content=response,
            timestamp=datetime.now().timestamp()
        ).save()
    except InvalidRequestError as error:
        print(error)
        response = (
            "Я только учусь и мне сложно анализировать "
            "так много сообщений в истории нашей переписки.\n"
            "Предлагаю сбросить контекст, и начать заново\n"
            "Для этого отправьте в чат /context и "
            "со всей силы нажмите на кнопку 'сбросить контекст'\n"
            "С момента этого нажатия контекст будет формироваться заново.")
    await update.message.reply_text(response)


async def make_picture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the image generated on request"""
    user = update.effective_user
    LOGGER.info(f"new_request: {user.id}; {user.mention_html()}; {update.message.text}")
    text_description = re.sub(f"/{PIC_COMMAND}", "", update.message.text)
    pic_url = get_gen_pic_url(text_description=text_description)
    print(pic_url)
    chat_id = update.effective_chat.id
    await context.bot.send_photo(chat_id=chat_id, photo=pic_url)


async def show_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send all current context"""
    user = update.effective_user
    LOGGER.info(f"new_request: {user.id}; {user.mention_html()}; {update.message.text}")
    context_all = get_last_n_message_tokens(user_id=user.id)
    LOGGER.info(f"new_request: {user.id}; {user.mention_html()}; {context_all}")
    if len(context_all) > 0:
        rows = ['{}: {}'.format(row['role'], row['content']) for row in context_all]
    else:
        rows = ['There is no context for now']
    [await update.message.reply_text(row) for row in rows]


async def choose_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wo_context = InlineKeyboardButton(text='без контекста', callback_data="context_0")
    last_10 = InlineKeyboardButton(text='последние N сообщений', callback_data="context_10")
    purge = InlineKeyboardButton(text='сбросить контекст', callback_data="context_purge")
    urlkb = InlineKeyboardMarkup(inline_keyboard=[[wo_context], [last_10], [purge]])
    await update.message.reply_text("вот", reply_markup=urlkb)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    user = update.effective_user
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    mes = f"Selected option: {query.data}"
    set_current_context(user=user, context_name=query.data)
    await query.answer(text=mes)


async def get_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """return user_info"""
    user = update.effective_user
    # print(user.id, user.full_name)
    await update.message.reply_text(text=f"User is {user.id}")
