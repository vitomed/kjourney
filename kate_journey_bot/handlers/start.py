from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from kate_journey_bot.config.logger import get_logger

logger = get_logger(__name__)


async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    logger.info(f"user_id: {user_id}")
    keyboard = [
        [InlineKeyboardButton("Экскурсия1", callback_data='tour_1')],
        [InlineKeyboardButton("Экскурсия2", callback_data='tour_2')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Я твой персональный гид-бот. Выбери маршрут:', reply_markup=reply_markup)
