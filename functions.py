from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

import markups as mrk
import texts as tx
from database import Database
from config import Config

LANGUAGE, CONTACT, GROUP, DAY, PAIR_NUM, BUILDING, ROOM, REASON, FINISH = range(9)

DB = Database()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.chat_id
    firstname = update.message.chat.first_name
    username = update.message.chat.username
    if not DB.check_user(user_id):
        DB.create_user({
            "user_id": user_id,
            "firstname": firstname,
            "username": username
        })
        await update.message.reply_text(
            text=tx.CHAT_TEXT['ru']['chose_lang'],
            reply_markup=mrk.language()
        )
        return LANGUAGE
    elif not DB.is_user_have_contact(user_id):
        await update.message.reply_text(
            text="Поделитесь вашим контактом",
            reply_markup=mrk.contact(text=tx.CHAT_TEXT['ru']['share_contact_button'])
        )
        return CONTACT
    else:
        lang = DB.get_lang(user_id)
        await update.message.reply_text(
            text=tx.CHAT_TEXT[lang]["for_send"],
            reply_markup=mrk.remove()
        )
        return GROUP


async def newrequest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.chat_id
    firstname = update.message.chat.first_name
    username = update.message.chat.username
    if not DB.check_user(user_id):
        DB.create_user({
            "user_id": user_id,
            "firstname": firstname,
            "username": username
        })
        await update.message.reply_text(
            text="Поделитесь вашим контактом",
            reply_markup=mrk.contact(text=tx.CHAT_TEXT['ru']['share_contact_button'])
        )
        return CONTACT
    else:
        lang = DB.get_lang(user_id)
        await update.message.reply_text(
            text=tx.CHAT_TEXT[lang]["for_send"],
            reply_markup=mrk.remove()
        )
        return GROUP


async def myrequests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    req = DB.get_all_requests(user_id)
    lang = DB.get_lang(user_id)
    if not req:
        await update.message.reply_text(
            text=tx.CHAT_TEXT[lang]["no_request"],

        )
    else:
        await update.message.reply_text(
            text=tx.CHAT_TEXT[lang]["all_requests"],
            reply_markup=mrk.all_requests(req, lang)
        )


async def change_language_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.message.chat_id
    data = update.callback_query.data.split('_')[-1]
    DB.update_user(user_id, key="lang", value=data)
    print("wewdwewe")
    await update.callback_query.message.edit_text(
        text=tx.CHAT_TEXT[data]['lang_changed']
    )
    await update.callback_query.message.reply_text(
        text=tx.CHAT_TEXT[data]['share_contact'],
        reply_markup=mrk.contact(text=tx.CHAT_TEXT[data]['share_contact_button'])
    )
    return CONTACT


async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    lang = DB.get_lang(user_id)
    await update.message.reply_text(
        text=tx.CHAT_TEXT[lang]['chose_lang'],
        reply_markup=mrk.language()
    )


async def language_change_success(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.message.chat_id
    data = update.callback_query.data.split('_')[-1]
    DB.update_user(user_id, key="lang", value=data)
    print('qwertyioopo')
    await update.callback_query.message.edit_text(
        text=tx.CHAT_TEXT[data]['lang_changed']
    )


async def myrequests_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.message.chat_id
    data = update.callback_query.data.split('_')[-1]
    lang = DB.get_lang(user_id)
    if data == 'back':
        req = DB.get_all_requests(user_id)
        if not req:
            await update.callback_query.message.edit_text(
                text=tx.CHAT_TEXT[lang]["no_request"],
            )
        else:
            await update.callback_query.message.edit_text(
                text=tx.CHAT_TEXT[lang]["all_requests"],
                reply_markup=mrk.all_requests(req, lang)
            )
    else:
        item = DB.get_request_button(user_id, data)
        status = tx.CHAT_TEXT[lang]['reject'] if item[7] == "rejected" else tx.CHAT_TEXT[lang]['accept'] if item[7] == "accepted" else tx.CHAT_TEXT[lang]['in_progress']
        await update.callback_query.message.edit_text(
            text=tx.FINAL_TEXT[lang].format(a=item, b=status),
            reply_markup=mrk.back_to_requests(lang),
            parse_mode="html"
        )


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.chat_id
    number = update.message.contact.phone_number
    lang = DB.get_lang(user_id)
    DB.update_user(user_id, "phone", number)
    await update.message.reply_text(
        text=tx.CHAT_TEXT[lang]["input_potok"],
        reply_markup=mrk.remove()
    )
    return GROUP


async def group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.chat_id
    data = update.message.text
    lang = DB.get_lang(user_id)

    if data == "back":
        await update.message.edit_text(
            text=tx.CHAT_TEXT[lang]["input_potok"],
            reply_markup=None
        )
        return GROUP
    if not DB.check_request(user_id):
        DB.create_request({
            "user_id": user_id,
            "potok": data
        })
    else:
        DB.update_request(user_id, 'potok', data)
    await update.message.reply_text(
        text=tx.CHAT_TEXT[lang]["chose_weekday"],
        reply_markup=mrk.weekdays(lang)
    )
    return DAY


async def weekday_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.callback_query.message.chat_id
    data = update.callback_query.data
    lang = DB.get_lang(user_id)
    if data == "back":
        await update.callback_query.message.edit_text(
            text=tx.CHAT_TEXT[lang]["input_potok"],
            reply_markup=None
        )
        return GROUP
    DB.update_request(user_id, 'weekday', tx.WEEDDAYS[lang].get(data.replace("week", "")))
    await update.callback_query.message.edit_text(
        text=tx.CHAT_TEXT[lang]["pair_num"],
        reply_markup=mrk.pair_nums(lang)
    )
    return PAIR_NUM


async def pair_num_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.callback_query.message.chat_id
    data = update.callback_query.data
    lang = DB.get_lang(user_id)
    if data == "back":
        await update.callback_query.message.edit_text(
            text=tx.CHAT_TEXT[lang]["chose_weekday"],
            reply_markup=mrk.weekdays(lang)
        )
        return DAY
        # await update.callback_query.message.edit_text(
        #     text="Выберите номер пары",
        #     reply_markup=mrk.pair_nums(lang)
        # )
        # return PAIR_NUM
    DB.update_request(user_id, 'pairnum', data.replace("pair_", ""))
    await update.callback_query.message.edit_text(
        text=tx.CHAT_TEXT[lang]["chose_pavilion"],
        reply_markup=mrk.building(lang)
    )
    return BUILDING


async def building_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.callback_query.message.chat_id
    data = update.callback_query.data
    msg_id = update.callback_query.message.message_id
    lang = DB.get_lang(user_id)
    if data == "back":
        await update.callback_query.message.edit_text(
            text=tx.CHAT_TEXT[lang]["pair_num"],
            reply_markup=mrk.pair_nums(lang)
        )
        return PAIR_NUM
        # await update.callback_query.message.edit_text(
        #     text="Выберите корпус",
        #     reply_markup=mrk.building(lang)
        # )
        # return BUILDING
    DB.update_request(user_id, 'campus', data.replace("building_", ""))
    # await update.callback_query.message.edit_text(
    #     text="Введите кабинет",
    # )
    await context.bot.delete_message(
        chat_id=user_id,
        message_id=msg_id
    )
    await context.bot.send_message(
        chat_id=user_id,
        text=tx.CHAT_TEXT[lang]["input_room_num"],
        reply_markup=mrk.back_button(lang)
    )
    return ROOM


async def room_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.chat_id
    msg_id = update.message.message_id
    data = update.message.text
    lang = DB.get_lang(user_id)
    if data == "⬅️Назад" or data == "⬅️Орқага":
        await context.bot.delete_message(user_id, msg_id-1)
        await context.bot.delete_message(user_id, msg_id)

        await context.bot.send_message(
            chat_id=user_id,
            text=tx.CHAT_TEXT[lang]["chose_pavilion"],
            reply_markup=mrk.building(lang)
        )
        return BUILDING

    DB.update_request(user_id, 'room', data)
    await update.message.reply_text(
        text=tx.CHAT_TEXT[lang]["change_reason"],
    )
    return REASON


async def reason_written(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.chat_id
    msg_id = update.message.message_id
    data = update.message.text
    lang = DB.get_lang(user_id)
    if data == "⬅️Назад" or data == "⬅️Орқага":
        await context.bot.delete_message(user_id, msg_id - 1)
        await context.bot.delete_message(user_id, msg_id)

        await context.bot.send_message(
            chat_id=user_id,
            text=tx.CHAT_TEXT[lang]["input_room_num"],
            reply_markup=mrk.back_button(lang)
        )
        return ROOM
    DB.update_request(user_id, 'reason', data)
    await update.message.reply_text(
        text=tx.CHAT_TEXT[lang]["request_sent"],
        reply_markup=mrk.remove()
    )
    request = DB.get_request(user_id)

    await context.bot.send_message(
        chat_id=int(Config.GROUP_ID),
        text=tx.RESULT_TEXT[lang].format(
            a=request
        ),
        parse_mode='html',
        reply_markup=mrk.accept_reject_buttons(user_id, request[0])
    )
    DB.update_request(user_id, 'status', "inprogress")
    return ConversationHandler.END

    # return FINISH


async def reject_or_accept(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # user_id = update.callback_query.message.chat_id
    user_id = update.callback_query.from_user.id
    lang = DB.get_lang(user_id)
    print(user_id)
    print(Config.ADMIN_ID)
    if user_id == int(Config.ADMIN_ID):
        data, user_id1, request_id = update.callback_query.data.split('_')
        request = DB.get_request(user_id1, request_id)
        if data == "accept":
            DB.update_request(user_id1, 'status', 'accepted', status="inprogress", request_id=request_id)
            await update.callback_query.message.edit_text(
                text=tx.FINAL_TEXT[lang].format(
                    a=request,
                    b=tx.CHAT_TEXT[lang]['accept']
                    # b="Одобрено✅"
                ), parse_mode="html"
            )
            await context.bot.send_message(
                user_id1,
                text=tx.FINAL_TEXT[lang].format(
                    a=request,
                    b=tx.CHAT_TEXT[lang]['accept']
                    # b="Одобрено✅"
                ), parse_mode="html"
            )
        elif data == "reject":
            DB.update_request(user_id1, 'status', 'rejected', status="inprogress", request_id=request_id)
            await update.callback_query.message.edit_text(
                text=tx.FINAL_TEXT[lang].format(
                    a=request,
                    b=tx.CHAT_TEXT[lang]['reject']
                    # b="Отказано❌"
                ), parse_mode="html"
            )
            await context.bot.send_message(
                user_id1,
                text=tx.FINAL_TEXT[lang].format(
                    a=request,
                    b=tx.CHAT_TEXT[lang]['reject']
                    # b="Отказано❌"
                ), parse_mode="html"
            )

        return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user_id = update.message.chat_id
    lang = DB.get_lang(user_id)
    await update.message.reply_text(
        text=tx.CHAT_TEXT[lang]['cancel']
    )

    return ConversationHandler.END
