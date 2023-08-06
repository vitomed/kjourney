from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from bot.config.logger import get_logger
from bot.tours import TOURS, PAYMENTS

ADMIN_IDs = [
    299234787,  # @vitomed
    # 5624161973  # @vmthai_phuket
    245160141  # @kate_katharsis
]

logger = get_logger(__name__)


async def request_tour(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    tour_key = update.message.text.split()[-1]  # assuming "/request tour1"
    logger.info(f"Пользователь user_id {user_id} username @{username} запрашивает доступ к tour_key {tour_key}.")
    if tour_key not in TOURS:
        await update.message.reply_text('Неправильный тур.')
        return

    keyboard = [
        [
            InlineKeyboardButton("Одобрить", callback_data=f'approve_{user_id}_{tour_key}_{username}'),
            InlineKeyboardButton("Отклонить", callback_data=f'deny_{user_id}_{tour_key}_{username}'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    for admin_id in ADMIN_IDs:
        await context.bot.send_message(chat_id=admin_id, text=f'Пользователь @{username} запрашивает доступ к экскурсии {tour_key}', reply_markup=reply_markup)


async def handle_admin_action(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    action, user_id, tour_key, username = query.data.split('_', 3)

    user_id = int(user_id)

    logger.info(f"администратор выполнил действие action: {action} user_id: {user_id} username: @{username} tour_key: {tour_key}")

    if action == "approve":
        if user_id not in PAYMENTS:
            PAYMENTS[user_id] = []
            logger.info(f"добавлен новый пользователь user_id {user_id} username @{username} в PAYMENTS.")
        PAYMENTS[user_id].append(tour_key)
        logger.info(f"пользователю user_id {user_id} username @{username} предоставлен доступ до экскурсии {tour_key}.")
    print(bool(action == 'approve' and tour_key in TOURS and user_id in PAYMENTS and tour_key in PAYMENTS[user_id]))
    print(action, tour_key, TOURS, user_id, PAYMENTS, tour_key, PAYMENTS[user_id])
    if action == 'approve' and tour_key in TOURS and user_id in PAYMENTS and tour_key in PAYMENTS[user_id]:
        await context.bot.send_message(chat_id=user_id, text=f'Ваш запрос на экскурсию {tour_key} одобрен. Спасибо за доверие и приятной экскурсии!')

    elif action == 'deny':
        await context.bot.send_message(chat_id=user_id, text=f'Ваш запрос на экскурсию {tour_key} отклонен.')

    await query.answer()