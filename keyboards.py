from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class MyPlaylistCallback(CallbackData, prefix="my playlist", sep=";"):
    id: int
    name: str


def my_playlist_keyboard_markup(my_playlist_list:list[dict], offset:int|None = None, skip:int|None = None):
   
    # Створюємо та налаштовуємо клавіатуру
    builder = InlineKeyboardBuilder()
    builder.adjust(1, repeat=True)


    for index, my_playlist_data in enumerate(my_playlist_list):
        # Створюємо об'єкт CallbackData
        callback_data = MyPlaylistCallback(id=index, **my_playlist_data)
        # Додаємо кнопку до клавіатури
        builder.button(
            text=f"{callback_data.name}",
            callback_data=callback_data.pack()
        )
    # Повертаємо клавіатуру у вигляді InlineKeyboardMarkup
    return builder.as_markup()
