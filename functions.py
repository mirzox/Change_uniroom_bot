from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

import markups as mrk
import texts as tx
from database import Database
from config import Config

CONTACT, GROUP, DAY, PAIR_NUM, BUILDING, ROOM, REASON, FINISH = range(8)

DB = Database()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.chat_id
    print(user_id)
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
            reply_markup=mrk.contact()
        )
        return CONTACT
    else:
        await update.message.reply_text(
            text="Для отправки заявки сначала введите поток",
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
            reply_markup=mrk.contact()
        )
        return CONTACT
    else:
        await update.message.reply_text(
            text="Для отправки заявки сначала введите поток",
            reply_markup=mrk.remove()
        )
        return GROUP


async def myrequests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    req = DB.get_all_requests(user_id)
    if not req:
        await update.message.reply_text(
            "У вас  еще нет запросов"
        )
    else:
        await update.message.reply_text(
            "Все ваши запросы: ",
            reply_markup=mrk.all_requests(req)
        )


async def myrequests_inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.message.chat_id
    data = update.callback_query.data.split('_')[-1]
    if data == 'back':
        req = DB.get_all_requests(user_id)
        if not req:
            await update.callback_query.message.edit_text(
                "У вас  еще нет запросов"
            )
        else:
            await update.callback_query.message.edit_text(
                text="Все ваши запросы: ",
                reply_markup=mrk.all_requests(req)
            )
    else:
        item = DB.get_request_button(user_id, data)
        status = "Отказано❌" if item[7]=="rejected" else "Одобрено✅" if item[7] == "accepted" else "В рассмотрении"
        await update.callback_query.message.edit_text(
            text=tx.FINAL_TEXT.format(a=item, b=status),
            reply_markup=mrk.back_to_requests(),
            parse_mode="html"
        )


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.chat_id
    number = update.message.contact.phone_number
    print(number)
    DB.update_user(user_id, "phone", number)
    await update.message.reply_text(
        text="Введите поток",
        reply_markup=mrk.remove()
    )
    return GROUP


async def group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.chat_id
    data = update.message.text
    if data == "back":
        await update.message.edit_text(
            text="Введите поток",
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
        text="Выберите день недели",
        reply_markup=mrk.weekdays()
    )
    return DAY


async def weekday_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.callback_query.message.chat_id
    data = update.callback_query.data
    if data == "back":
        await update.callback_query.message.edit_text(
            text="Введите поток",
            reply_markup=None
        )
        return GROUP
    DB.update_request(user_id, 'weekday', tx.WEEDDAYS.get(data.replace("week", "")))
    await update.callback_query.message.edit_text(
        text="Выберите номер пары",
        reply_markup=mrk.pair_nums()
    )
    return PAIR_NUM


async def pair_num_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.callback_query.message.chat_id
    data = update.callback_query.data
    if data == "back":
        await update.callback_query.message.edit_text(
            text="Выберите день недели",
            reply_markup=mrk.weekdays()
        )
        return DAY
        # await update.callback_query.message.edit_text(
        #     text="Выберите номер пары",
        #     reply_markup=mrk.pair_nums()
        # )
        # return PAIR_NUM
    DB.update_request(user_id, 'pairnum', data.replace("pair_", ""))
    await update.callback_query.message.edit_text(
        text="Выберите корпус",
        reply_markup=mrk.building()
    )
    return BUILDING


async def building_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.callback_query.message.chat_id
    data = update.callback_query.data
    msg_id = update.callback_query.message.message_id
    if data == "back":
        await update.callback_query.message.edit_text(
            text="Выберите номер пары",
            reply_markup=mrk.pair_nums()
        )
        return PAIR_NUM
        # await update.callback_query.message.edit_text(
        #     text="Выберите корпус",
        #     reply_markup=mrk.building()
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
        text="Введите кабинет",
        reply_markup=mrk.back_button()
    )
    return ROOM


async def room_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.chat_id
    msg_id = update.message.message_id
    data = update.message.text
    if data == "⬅️Назад":
        await context.bot.delete_message(user_id, msg_id-1)
        await context.bot.delete_message(user_id, msg_id)

        await context.bot.send_message(
            chat_id=user_id,
            text="Выберите корпус",
            reply_markup=mrk.building()
        )
        return BUILDING

    DB.update_request(user_id, 'room', data)
    await update.message.reply_text(
        text="Введите причину по которой хотите поменять пару"
    )
    return REASON


async def reason_written(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.chat_id
    msg_id = update.message.message_id
    data = update.message.text
    if data == "⬅️Назад":
        await context.bot.delete_message(user_id, msg_id - 1)
        await context.bot.delete_message(user_id, msg_id)

        await context.bot.send_message(
            chat_id=user_id,
            text="Введите кабинет",
            reply_markup=mrk.back_button()
        )
        return ROOM
    DB.update_request(user_id, 'reason', data)
    await update.message.reply_text(
        text="Ваша заявка успешно оформлено ждите ответа через бот",
        reply_markup=mrk.remove()
    )
    request = DB.get_request(user_id)

    await context.bot.send_message(
        chat_id=int(Config.GROUP_ID),
        text=tx.RESULT_TEXT.format(
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
    print(user_id)
    print(Config.ADMIN_ID)
    if user_id == int(Config.ADMIN_ID):
        data, user_id1, request_id = update.callback_query.data.split('_')
        request = DB.get_request(user_id1, request_id)
        if data == "accept":
            DB.update_request(user_id1, 'status', 'accepted', status="inprogress", request_id=request_id)
            await update.callback_query.message.edit_text(
                text=tx.FINAL_TEXT.format(
                    a=request,
                    b="Одобрено✅"
                ), parse_mode="html"
            )
            await context.bot.send_message(
                user_id1,
                text=tx.FINAL_TEXT.format(
                    a=request,
                    b="Одобрено✅"
                ), parse_mode="html"
            )
        elif data == "reject":
            DB.update_request(user_id1, 'status', 'rejected', status="inprogress", request_id=request_id)
            await update.callback_query.message.edit_text(
                text=tx.FINAL_TEXT.format(
                    a=request,
                    b="Отказано❌"
                ), parse_mode="html"
            )
            await context.bot.send_message(
                user_id1,
                text=tx.FINAL_TEXT.format(
                    a=request,
                    b="Отказано❌"
                ), parse_mode="html"
            )

        return ConversationHandler.END
