import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, URLInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiohttp import ClientSession
from aiohttp.client_exceptions import InvalidURL
from commands import (
    MY_PLAYLIST_COMMAND,
    START_COMMAND,
    SONG_ADD_COMMAND,
    # SONG_DELETE_COMMAND,
    BOT_COMMANDS,
)
from data import get_data, add_songs
from keyboards import my_playlist_keyboard_markup, MyPlaylistCallback
from utiels import async_log_function_call
from models import MyPlaylist, SongForm
from config import BOT_TOKEN as TOKEN

dp = Dispatcher()


@dp.message(START_COMMAND)
@async_log_function_call
async def start(
    message: Message,
    *args,
    **kwargs,
) -> None:
    message_text = (
        f"Hello, {html.bold(message.from_user.full_name)}!\n"
        "I'm the bot that will be helping you to store your music in one place."
    )
    await message.answer(text=message_text)


@dp.message(MY_PLAYLIST_COMMAND)
@async_log_function_call
async def my_playlist(
    message: Message,
    *args,
    **kwargs,
) -> None:
    data = get_data()
    markup = my_playlist_keyboard_markup(my_playlist_list=data.get("my_playlist"))
    message_text = f"Your songs."
    await message.answer(
        text=message_text,
        reply_markup=markup,
    )


# @dp.message(SONG_DELETE_COMMAND)
# @async_log_function_call
# async def delete_song(message: Message, *args, **kwargs,) -> None:


@dp.message(SONG_ADD_COMMAND)
@async_log_function_call
async def add_song(
    message: Message,
    state: FSMContext,
    *args,
    **kwargs,
) -> None:
    await state.set_state(SongForm.name)
    await message.answer(
        f"Enter song name.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(SongForm.name)
@async_log_function_call
async def song_name(
    message: Message,
    state: FSMContext,
    *args,
    **kwargs,
) -> None:
    await state.update_data(name=message.text)
    await state.set_state(SongForm.duration)
    await message.answer(
        f"Enter how long is the song.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(SongForm.duration)
@async_log_function_call
async def song_duration(
    message: Message,
    state: FSMContext,
    *args,
    **kwargs,
) -> None:
    await state.update_data(duration=message.text)
    await state.set_state(SongForm.genre)
    await message.answer(
        f"Enter what genre is the song in.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(SongForm.genre)
@async_log_function_call
async def song_genre(
    message: Message,
    state: FSMContext,
    *args,
    **kwargs,
) -> None:
    await state.update_data(genre=message.text)
    await state.set_state(SongForm.author)
    message_text = f"Enter authors of the song rith a coma after each one ', '"
    message_text += html.bold("Coma is important.")
    await message.answer(
        text=message_text,
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(SongForm.author)
@async_log_function_call
async def song_author(
    message: Message,
    state: FSMContext,
    *args,
    **kwargs,
) -> None:
    data = await state.update_data(author=message.text.split(", "))
    await state.set_state(SongForm.cover)
    await message.answer(
        f"Enter a link to the cover of the song",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(SongForm.cover)
@async_log_function_call
async def song_cover(
    message: Message,
    state: FSMContext,
    *args,
    **kwargs,
) -> None:
    data = await state.update_data(cover=message.text)
    song = MyPlaylist(**data)
    add_songs(song.model_dump())
    await state.clear()
    await message.answer(
        f"Song {song.name} added",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.callback_query(MyPlaylistCallback.filter())
@async_log_function_call
async def callb_my_playlist(
    callback: CallbackQuery,
    callback_data: MyPlaylistCallback,
    *args,
    **kwargs,
) -> None:
    my_playlist_id = callback_data.id
    my_playlist_data = get_data(my_playlist_id=my_playlist_id)
    my_playlist = MyPlaylist(**my_playlist_data)

    text = (
        f"song: {my_playlist.name}\n"
        f"duration: {my_playlist.duration}\n"
        f"genre: {my_playlist.genre}\n"
        f"author: {', '.join(my_playlist.author)}\n"
    )
    if await check_url(my_playlist.cover):

        photo = URLInputFile(
            my_playlist.cover,
            filename=f"{my_playlist.name}_cover.{my_playlist.cover.split('.')[-1]}",
        )

        await callback.message.answer_photo(
            # text=text,
            caption=text,
            photo=photo
        )
    else:
        await callback.message.answer(text=text)


async def check_url(url):
    is_correct = False
    try:
        async with ClientSession() as session:
            async with session.get(url) as resp:
                await resp.text()
                if resp.status == 200:
                    print(resp.status)
                    exit()
                    is_correct = True
    except InvalidURL:
        ...
    finally:
        return is_correct

    


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


@async_log_function_call
async def main(
    *args,
    **kwargs,
) -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(BOT_COMMANDS)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
