from telegram.ext import (
    CommandHandler,
    PicklePersistence,
    ApplicationBuilder, CallbackQueryHandler
)

from . import handlers
from .config.access import TOKEN
from .config.logger import get_logger

COMMAND_HANDLERS = {
    "start": handlers.start,
    "request": handlers.request_tour,
}

CALLBACK_QUERY_HANDLERS = {
    "^(approve|deny)": handlers.handle_admin_action
}

logger = get_logger(__name__)


def main() -> None:
    persistence = PicklePersistence(filepath="backup")
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .persistence(persistence)
        .build()
    )
    for command_name, command_handler in COMMAND_HANDLERS.items():
        application.add_handler(CommandHandler(command_name, command_handler))

    for pattern, command_handler in CALLBACK_QUERY_HANDLERS.items():
        application.add_handler(CallbackQueryHandler(command_handler, pattern=pattern))
    application.add_handler(CallbackQueryHandler(handlers.button))

    application.run_polling()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())
