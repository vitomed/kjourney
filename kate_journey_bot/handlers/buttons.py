import time

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import CallbackContext
from jinja2 import Environment, FileSystemLoader

from kate_journey_bot.config.logger import get_logger
from kate_journey_bot.tours import TOURS, PAYMENTS

logger = get_logger(__name__)

env = Environment(loader=FileSystemLoader('templates'))


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id  # для того, чтобы отправить соообщение а не перезатирать его
    user_id = query.from_user.id

    await query.answer()

    data = query.data.split("_")
    tour_key = data[1]
    logger.info(f"tour_id: {tour_key}")
    stage_idx = int(data[2]) if len(data) == 3 else 0
    logger.info(f"stage_idx: {stage_idx}")

    if user_id not in PAYMENTS or tour_key not in PAYMENTS[user_id]:
        await context.bot.send_message(chat_id=chat_id, text='Вы еще не оплатили этот тур!')
        return

    if stage_idx == 0:
        await context.bot.send_message(chat_id=chat_id, text=f'Вы выбрали экскурсию {tour_key}. Приятного путешествия!')
        context.user_data['chosen_tour'] = tour_key
        # time.sleep(1)

    if stage_idx < len(TOURS[tour_key]):
        keyboard = [[InlineKeyboardButton("Далее", callback_data=f'tour_{tour_key}_{stage_idx + 1}')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        template = env.get_template(TOURS[tour_key][stage_idx])
        result = template.render()

        # await query.edit_message_text(text=TOURS[tour_id][section_number], reply_markup=reply_markup)
        await context.bot.send_message(
            chat_id=chat_id, text=result, reply_markup=reply_markup, parse_mode=ParseMode.HTML
        )
    else:
        # await query.edit_message_text(text="Спасибо за участие в экскурсии!")
        await context.bot.send_message(chat_id=chat_id, text="Спасибо за участие в экскурсии!")

