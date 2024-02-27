

RESULT_TEXT = {
    "uz": """
Телефон раками:  {phone}    
    
Сўров № <b>{a[0]}</b>
Поток: <b>{a[1]}</b>
Кун: <b>{a[2]}</b>
Жуфтлик рақами: <b>{a[3]}</b>
Бино: <b>{a[4]}</b>
Ўқув ҳонаси: <b>{a[5]}</b>
Сабаб: <b>{a[6]}</b>
    """,
    "ru": """
Номер телефона:  {phone}    

Запрос № <b>{a[0]}</b>
Поток: <b>{a[1]}</b>
День недели: <b>{a[2]}</b>
Номер пары: <b>{a[3]}</b>
Корпус: <b>{a[4]}</b>
Кабинет: <b>{a[5]}</b>
Причина: <b>{a[6]}</b>

    """
}


FINAL_TEXT = {
    "uz": """
Сўров № <b>{a[0]}</b>
Поток: <b>{a[1]}</b>
Кун: <b>{a[2]}</b>
Жуфтлик рақами: <b>{a[3]}</b>
Бино: <b>{a[4]}</b>
Ўқув ҳонаси: <b>{a[5]}</b>
Сабаб: <b>{a[6]}</b>

Статус: <b>{b}</b>
    """,
    "ru": """
Запрос № <b>{a[0]}</b>
Поток: <b>{a[1]}</b>
День недели: <b>{a[2]}</b>
Номер пары: <b>{a[3]}</b>
Корпус: <b>{a[4]}</b>
Кабинет: <b>{a[5]}</b>
Причина: <b>{a[6]}</b>

Статус: <b>{b}</b>
    """
}

WEEDDAYS = {
    "uz": {
        "1": "Душанба",
        "2": "Сешанба",
        "3": "Чорщанба",
        "4": "Пайшанба",
        "5": "Жума",
        "6": "Шанба",
        "7": "Якшанба"
    },
    "ru": {
        "1": "Понедельник",
        "2": "Вторник",
        "3": "Среда",
        "4": "Четверг",
        "5": "Пятница",
        "6": "Суббота",
        "7": "Воскресенье"
    }
}

CHAT_TEXT = {
    "uz": {
        "share_contact": "Контактингизни юборинг",
        "share_contact_button": "Контактни юборинг",
        "for_send": "Сўровни юбориш учун аввал потокни киритинг",
        "no_request": "Сизда ҳали ҳеч қандай сўров йўқ",
        "all_requests": "Барча сўровларингиз",
        "chose_lang": "Тилни танланг",
        "lang_changed": "Сиз тилни ўзгартирдингиз",
        "reject": "Рад этилди❌",
        "accept": "Тасдиқланди✅",
        "in_progress": "Кўриб чиқилмоқда",
        "input_potok": "Потокни киритинг",
        "chose_weekday": "Ҳафта кунини танланг",
        "pair_num": "Жуфтлик рақамини танланг",
        "chose_pavilion": "Бинони танланг",
        "input_room_num": "Ўқув ҳонани рақамини киритинг",
        "change_reason": "Ўқув ҳонани ўзгартирмоқчи бўлган сабабни киритинг",
        "request_sent": "Aризангиз муваффақиятли якунланди, жавобни кутинг",
        "back": "⬅️Орқага",
        "cancel": "Бот тўхтатилди, янги сўровни жонатиш учун /start ёки /newrequest буйруғини юборинг"

    },
    "ru": {
        "share_contact": "Поделитесь вашим контактом",
        "share_contact_button": "Отправить контакт",
        "for_send": "Для отправки заявки, введите поток",
        "no_request": "У вас еще нет запросов",
        "all_requests": "Все ваши запросы: ",
        "chose_lang": "Выберите язык",
        "lang_changed": "Вы успешно поменяли язык",
        "reject": "Отказано❌",
        "accept": "Одобрено✅",
        "in_progress": "В рассмотрении",
        "input_potok": "Введите поток",
        "chose_weekday": "Выберите день недели",
        "pair_num": "Выберите номер пары",
        "chose_pavilion": "Выберите корпус",
        "input_room_num": "Введите номер аудитории",
        "change_reason": "Введите причину по которой хотите поменять аудиторию",
        "request_sent": "Ваша заявка успешно оформлена, ждите ответа",
        "back": "⬅️Назад",
        "cancel": "Бот был остановлен, чтобы отправить новый запрос отправьте команду /start или /newrequest"
    }
}
