from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

MY_PLAYLIST_COMMAND = Command("playlist")
START_COMMAND = Command("start")
SONG_ADD_COMMAND = Command("add_song")
#SONG_DELETE_COMMAND = Command("delete_song")

MY_PLAYLIST_BOT_COMMAND = BotCommand(command="playlist", description="Your playlist"),
START_BOT_COMMAND = BotCommand(command="start", description="Start the Bot"),
SONG_ADD_BOT_COMMAND = BotCommand(command="add_song", description="add a new song to your playlist"),
#SONG_DELETE_BOT_COMMAND = BotCommand(command="delete_song", description="delete a song from your playlist"),

BOT_COMMANDS = [
    BotCommand(command="playlist", description="Your playlist"),
    BotCommand(command="start", description="Start the Bot"),
    BotCommand(command="add_song", description="add a new song to your playlist"),
    #BotCommand(command="delete_song", description="delete a song from your playlist"),
]