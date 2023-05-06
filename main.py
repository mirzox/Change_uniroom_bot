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
    reject_or_accept
)

from config import Config

CONTACT, GROUP, DAY, PAIR_NUM, BUILDING, ROOM, REASON, FINISH = range(8)


def main() -> None:
    app = Application.builder().token(Config.API_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CommandHandler('newrequest', newrequest)],
        states={
            CONTACT: [MessageHandler(filters=filters.CONTACT, callback=contact)],
            GROUP: [MessageHandler(filters=filters.TEXT, callback=group)],
            DAY: [CallbackQueryHandler(pattern="^week|back", callback=weekday_chosen)],
            PAIR_NUM: [CallbackQueryHandler(pattern="^pair|back", callback=pair_num_chosen)],
            BUILDING: [CallbackQueryHandler(pattern="^building|back", callback=building_chosen)],
            ROOM: [MessageHandler(filters=filters.TEXT, callback=room_chosen)],
            REASON: [MessageHandler(filters=filters.TEXT, callback=reason_written)],
        },
        fallbacks=[],
        per_chat=True,
        # per_message=True

    )
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(pattern="^accept|reject", callback=reject_or_accept))
    app.add_handler(CommandHandler('myrequests', myrequests))
    app.add_handler(CallbackQueryHandler(pattern="^request", callback=myrequests_inline))
    app.run_polling()


if __name__ == "__main__":
    main()
