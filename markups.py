from typing import List
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


def build_menu(buttons: List, n_cols: int, header_buttons=None, footer_buttons=None) -> List[List]:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        for i in footer_buttons:
            menu.append([i])
    return menu


def contact(text) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([[KeyboardButton(text=text, request_contact=True)]],
                               resize_keyboard=True, one_time_keyboard=True
                               )


def language() -> InlineKeyboardMarkup:
    items = [
        InlineKeyboardButton(text="Узбек 🇺🇿", callback_data="lang_uz"),
        InlineKeyboardButton(text="Русский 🇷🇺", callback_data="lang_ru")
    ]
    return InlineKeyboardMarkup(build_menu(items, 2))


def start_language() -> InlineKeyboardMarkup:
    items = [
        InlineKeyboardButton(text="Узбек 🇺🇿", callback_data="start_lang_uz"),
        InlineKeyboardButton(text="Русский 🇷🇺", callback_data="start_lang_ru")
    ]
    return InlineKeyboardMarkup(build_menu(items, 2))


def remove() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()


def weekdays(lang) -> InlineKeyboardMarkup:
    if lang == 'uz':
        week_days = [
        "Душанба",
        "Сешанба",
        "Чорщанба",
        "Пайшанба",
        "Жума",
        "Шанба",
        ]
        footer = [InlineKeyboardButton(text="⬅️Орқага", callback_data="back")]

    else:
        week_days = [
            "Понедельник",
            "Вторник",
            "Среда",
            "Четверг",
            "Пятница",
            "Суббота",
        ]
        # items = [
        #     InlineKeyboardButton(text="Понедельник", callback_data="week1"),
        #     InlineKeyboardButton(text="Вторник", callback_data="week2"),
        #     InlineKeyboardButton(text="Среда", callback_data="week3"),
        #     InlineKeyboardButton(text="Четверг", callback_data="week4"),
        #     InlineKeyboardButton(text="Пятница", callback_data="week5"),
        #     InlineKeyboardButton(text="Суббота", callback_data="week6"),
        # ]
        footer = [InlineKeyboardButton(text="⬅️Назад", callback_data="back")]

    items = [
        InlineKeyboardButton(text=j, callback_data=f"week{i + 1}") for i, j in enumerate(week_days)
    ]
    return InlineKeyboardMarkup(build_menu(items, 2, footer_buttons=footer))


def pair_nums(lang='ru') -> InlineKeyboardMarkup:
    if lang == 'uz':
        footer = [InlineKeyboardButton(text="⬅️Орқага", callback_data="back")]
    else:
        footer = [InlineKeyboardButton(text="⬅️Назад", callback_data="back")]
    return InlineKeyboardMarkup(build_menu(
        [InlineKeyboardButton(text=f"{i}", callback_data=f"pair_{i}") for i in range(1, 7)], 2,
        footer_buttons=footer
    ))


def building(lang='ru') -> InlineKeyboardMarkup:
    items = [
        InlineKeyboardButton(text="A", callback_data="building_A"),
        InlineKeyboardButton(text="B", callback_data="building_B"),
        InlineKeyboardButton(text="C", callback_data="building_C"),
        InlineKeyboardButton(text="D", callback_data="building_D"),
        InlineKeyboardButton(text="E", callback_data="building_E"),
        InlineKeyboardButton(text="F", callback_data="building_F"),
    ]
    if lang == 'uz':
        footer = [InlineKeyboardButton(text="⬅️Орқага", callback_data="back")]
    else:
        footer = [InlineKeyboardButton(text="⬅️Назад", callback_data="back")]
    return InlineKeyboardMarkup(build_menu(items, 2, footer_buttons=footer))


def back_button(lang) -> ReplyKeyboardMarkup:
    if lang == 'uz':
        return ReplyKeyboardMarkup([[KeyboardButton(text="⬅️Орқага")]], resize_keyboard=True, one_time_keyboard=True)
    return ReplyKeyboardMarkup([[KeyboardButton(text="⬅️Назад")]], resize_keyboard=True, one_time_keyboard=True)


def accept_reject_buttons(user_id, request_id):
    items = [
        InlineKeyboardButton(text="Принять✅", callback_data=f"accept_{user_id}_{request_id}"),
        InlineKeyboardButton(text="Отказать❌", callback_data=f"reject_{user_id}_{request_id}")
    ]
    return InlineKeyboardMarkup(build_menu(items, 2))


def all_requests(items, lang='ru') -> InlineKeyboardMarkup:
    if lang == 'uz':
        keyboards = [
            InlineKeyboardButton(text=f"Сўров: {i[0]} Поток: {i[1]}", callback_data=f"request_{i[0]}") for i in items
        ]
    else:
        keyboards = [
            InlineKeyboardButton(text=f"Запрос: {i[0]} Поток: {i[1]}", callback_data=f"request_{i[0]}") for i in items
        ]
    return InlineKeyboardMarkup(build_menu(keyboards, 1))


def back_to_requests(lang) -> InlineKeyboardMarkup:
    if lang == 'uz':
        return InlineKeyboardMarkup(
            build_menu([InlineKeyboardButton(text="⬅️Орқага", callback_data="request_back", )], 1))

    return InlineKeyboardMarkup(build_menu([InlineKeyboardButton(text="⬅️Назад", callback_data="request_back", )], 1))
