from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from functions import (
    start,
    newrequest,
    myrequests,
    myrequests_inline,
    contact,
    group,
    weekday_chosen,
    pair_num_chosen,
    building_chosen,
    room_chosen,
    reason_written,
    reject_or_accept,
    change_language,
    language_change_success,
    cancel,
    change_language_start
)

from config import Config

LANGUAGE, CONTACT, GROUP, DAY, PAIR_NUM, BUILDING, ROOM, REASON, FINISH = range(9)


def main() -> None:
    app = Application.builder().token(Config.API_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CommandHandler('newrequest', newrequest)],
        states={
            LANGUAGE: [CallbackQueryHandler(pattern="^lang_", callback=change_language_start)],
            CONTACT: [MessageHandler(filters=filters.CONTACT, callback=contact)],
            GROUP: [MessageHandler(filters=filters.TEXT & (~ filters.COMMAND), callback=group)],
            DAY: [CallbackQueryHandler(pattern="^week|back", callback=weekday_chosen)],
            PAIR_NUM: [CallbackQueryHandler(pattern="^pair|back", callback=pair_num_chosen)],
            BUILDING: [CallbackQueryHandler(pattern="^building|back", callback=building_chosen)],
            ROOM: [MessageHandler(filters=filters.TEXT & (~ filters.COMMAND), callback=room_chosen)],
            REASON: [MessageHandler(filters=filters.TEXT & (~ filters.COMMAND), callback=reason_written)],
        },
        fallbacks=[CommandHandler("stop", cancel)],
        per_chat=True,
        # per_message=True

    )
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('myrequests', myrequests))
    app.add_handler(CommandHandler("change_language", change_language))

    app.add_handler(CallbackQueryHandler(pattern="^accept|reject", callback=reject_or_accept))
    app.add_handler(CallbackQueryHandler(pattern="^request", callback=myrequests_inline))
    app.add_handler(CallbackQueryHandler(pattern="^lang_", callback=language_change_success))
    app.run_polling()


if __name__ == "__main__":
    main()
