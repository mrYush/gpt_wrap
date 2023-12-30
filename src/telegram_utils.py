"""Module for telegram handlers"""
import logging
import re
from datetime import datetime

from telegram import Update, ForceReply, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram.ext import ContextTypes

from db_utils.scheme import set_current_context, ConversationCollection, \
    get_last_messages, check_user, PictureCollection
from gpt_utils import get_answer, get_gen_pic_url
from settings import TELEGRAM_ID_FOR_CONNECTION

LOGGER = logging.getLogger()
PIC_COMMAND = "pic"
SHOW_CONTEXT = 'show_context'
CONTEXT = 'context'


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
    limit_msg = mongo_user.limit_msg
    if limit_msg is None:
        limit_msg = 200
        # add limit_msg to mongo_user
        mongo_user.update(limit_msg=limit_msg)
    today_generated_count = ConversationCollection.objects(
        telegram_id=user.id,
        timestamp__gte=datetime.now().timestamp() - 24 * 60 * 60
    ).count()
    if today_generated_count >= limit_msg:
        text = (f"Sorry, but you have reached your limit of {limit_msg} "
                f"messages per day. "
                f"Please, connect to {TELEGRAM_ID_FOR_CONNECTION} "
                f"for increasing your limit.")
        await update.message.reply_text(
            text=text,
        )
        return
    else:
        # current_context = mongo_user.current_context
        system_prompt = mongo_user.system_prompt
        request = update.message.text
        ConversationCollection(
            telegram_id=user.id,
            context_id=mongo_user.current_context,
            role='user',
            content=request,
            timestamp=datetime.now().timestamp()
        ).save()
        if mongo_user.start_context_timestamp is None:
            start_from_timestamp = 0
        else:
            start_from_timestamp = mongo_user.start_context_timestamp
        kwargs = {'messages': get_last_messages(
            user_id=user.id,
            system_prompt=system_prompt,
            start_from_timestamp=start_from_timestamp
        )}
        try:
            response = get_answer(**kwargs)
            ConversationCollection(
                telegram_id=user.id,
                context_id=mongo_user.current_context,
                role='assistant',
                content=response,
                timestamp=datetime.now().timestamp()
            ).save()
        except Exception as error:
            LOGGER.error(error)
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
    mongo_user = check_user(user=user, return_mongo_user=True)
    limit_pic = mongo_user.limit_pic
    if limit_pic is None:
        limit_pic = 100
        mongo_user.update(limit_pic=limit_pic)
    today_generated_count = PictureCollection.objects(
        telegram_id=user.id,
        timestamp__gte=datetime.now().timestamp() - 24 * 60 * 60
    ).count()
    if today_generated_count >= limit_pic:
        text = (f"Sorry, but you have reached your limit of {limit_pic} "
                f"pictures per day. "
                f"Please, connect to {TELEGRAM_ID_FOR_CONNECTION} "
                f"for increasing your limit.")
        await update.message.reply_text(
            text=text,
        )
        return
    else:
        LOGGER.info(
            f"new_request: {user.id}; {user.mention_html()}; {update.message.text}")
        text_description = re.sub(f"/{PIC_COMMAND}", "", update.message.text)
        pic_url = get_gen_pic_url(text_description=text_description)
        print(pic_url)
        chat_id = update.effective_chat.id
        await context.bot.send_photo(chat_id=chat_id, photo=pic_url)
        PictureCollection(
            telegram_id=user.id,
            timestamp=datetime.now().timestamp(),
            prompt=text_description,
            url=pic_url
        ).save()


async def show_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send all current context"""
    user = update.effective_user
    context_all = get_last_messages(user_id=user.id)
    if len(context_all) > 0:
        rows = ['{}: {}'.format(row['role'], row['content']) for row in
                context_all]
    else:
        rows = ['There is no context for now']
    [await update.message.reply_text(row) for row in rows]


async def choose_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    purge = InlineKeyboardButton(text='сбросить контекст',
                                 callback_data="context_purge")
    urlkb = InlineKeyboardMarkup(inline_keyboard=[[purge]])
    await update.message.reply_text("вот", reply_markup=urlkb)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    user = update.effective_user
    mes = f"Selected option: {query.data}"
    set_current_context(user=user, context_name=query.data)
    await query.answer(text=mes)


async def get_user_info(update: Update,
                        context: ContextTypes.DEFAULT_TYPE) -> None:
    """return user_info"""
    user = update.effective_user
    # print(user.id, user.full_name)
    await update.message.reply_text(text=f"User is {user.id}")


async def set_system_prompt(update: Update,
                            context: ContextTypes.DEFAULT_TYPE) -> None:
    """return user_info"""
    user = update.effective_user
    mongo_user = check_user(user=user, return_mongo_user=True)
    mongo_user.update(system_prompt=update.message.text)
    await update.message.reply_text(
        text=f"System prompt {update.message.text} is set"
    )
