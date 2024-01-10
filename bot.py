import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton 
from aiogram import F
from aiogram.fsm.context import FSMContext
import i18n
from helpers.helpers import (
    File, get_language,
    transcipt_file, initialize_languages,
    ask_and_save, downloader
    )
from helpers.database_connector import SQLiteConnector

filearray = [File(),File(),File(),File(),File()]



#locales, json preferable, removing namespace
i18n.load_path.append('locales')
i18n.set('file_format', 'json')
i18n.set('filename_format', '{locale}.{format}')


#database connect
db = SQLiteConnector("database\\users.db")


#key for openaiprompt in the helpers.py

#telegram key
TOKEN_API = "6868575277:AAEASpqAYf0rIbtDSSNq5JUAJgLYjAba7aU"
bot = Bot(TOKEN_API)

dp = Dispatcher()

#BUTTONS AND KEYBOARDS
def start_chat_kb(id):
    button_start_chat = KeyboardButton(text=i18n.t("start_chat", locale=get_language(id)))
    return ReplyKeyboardMarkup(keyboard=[[button_start_chat]],resize_keyboard=True, one_time_keyboard=True)
def end_chat_kb(id):
    button_end_chat = KeyboardButton(text=i18n.t("end_chat", locale=get_language(id)))
    return ReplyKeyboardMarkup(keyboard=[[button_end_chat]],resize_keyboard=True, one_time_keyboard=True)

language_kb = initialize_languages()


#First call for the buttons to appear
@dp.message(F.text, Command("start"), StateFilter(None))
async def button_start(message: types.Message, state:FSMContext):
    id = message.from_user.id
    current = db.fetch_data_one("SELECT id FROM users WHERE id = ?", (id,))
    if current is None: db.execute_query("INSERT INTO users (id, chat, language) VALUES (?,?,?)", (id, "", ""))
    route_initialization()
    await state.set_state("Language_select")
    await message.reply("First of all, select your language!", reply_markup = language_kb)


#Handler for wrong input
@dp.message(F.text, StateFilter(None))
async def mistake_handler(message: types.Message):
    await message.reply("support")


@dp.message(F.photo | F.sticker | F.video | F.document)
async def wrong_type_handler(message: types.Message):
    await message.reply(text=i18n.t("support", locale=get_language(message.from_user.id)))


@dp.message(F.text, StateFilter("Language_select"))
async def language_switch(message: types.Message, state: FSMContext):
    id = message.from_user.id
    if message.text == u"\U0001F1FA\U0001F1E6":#ukraine unicode
        ln = 'ua'
    else:
        ln = 'en'
    db.execute_query("UPDATE users SET language = ? WHERE id = ?", (ln, id))
    await state.clear()
    await state.set_state("Ready")
    await message.reply(i18n.t("select", locale=ln), reply_markup=start_chat_kb(id))


@dp.message(F.text, Command("clear_state"))
async def clear_state_f(message: types.Message, state: FSMContext):
    await state.clear()


#route for handling the button press
#@dp.message(F.text == i18n.t("start_chat"), StateFilter("Ready"))
async def get_prompt(message: types.Message, state: FSMContext):
    id = message.from_user.id
    await message.reply(i18n.t("you_are_welcome", locale=get_language(id)), reply_markup = end_chat_kb(id))
    await state.clear()
    await state.set_state("waiting for prompt")


#@dp.message(F.text == i18n.t("end_chat"), StateFilter("waiting for prompt"))
async def end_chat(message: types.Message, state: FSMContext):
    id = message.from_user.id
    db.execute_query("UPDATE users SET chat = ? WHERE id = ?", ("", id))
    await message.reply(i18n.t("finish",locale=get_language(id)), reply_markup = start_chat_kb(id))
    await state.clear()
    await state.set_state("Ready")


#function for handling my input after prompt button has been used
#@dp.message(F.text, StateFilter("waiting for prompt"))
async def text_handler(message: types.Message, state: FSMContext):
    id = message.from_user.id
    request = message.text
    result = ask_and_save(request, id)
    await message.reply(result, parse_mode="MarkdownV2")

    
#@dp.message(F.voice, StateFilter("waiting for prompt"))
async def voice_handler(message: types.Message,  state: FSMContext):
    id = message.from_user.id
    checkFree = await downloader(bot, filearray, message)
    with open (checkFree[1], 'rb+') as audio_message:
        audio_text = transcipt_file(audio_message)
        filearray[checkFree[0]].switch()

    result = ask_and_save(audio_text, id)
    
    await message.reply(result, parse_mode="MarkdownV2")


@dp.message(F.text, Command("use"), StateFilter("Ready"))
async def print_info(message: types.Message):
    id = message.from_user.id
    data = (i18n.t("use", locale = get_language(id)))
    await message.answer(data)


@dp.message(F.text, Command("info"), StateFilter("Ready"))
async def print_info(message: types.Message):
    id = message.from_user.id
    data = (i18n.t("info", locale = get_language(id)))
    await message.answer(data)

#defining routes for locales
def route_initialization():
    dp.message.register(get_prompt, F.text == i18n.t("start_chat", locale='en'), StateFilter("Ready"))
    dp.message.register(get_prompt, F.text == i18n.t("start_chat", locale='ua'), StateFilter("Ready"))
    dp.message.register(end_chat, F.text == i18n.t("end_chat",locale='en'), StateFilter("waiting for prompt"))
    dp.message.register(end_chat, F.text == i18n.t("end_chat",locale='ua'), StateFilter("waiting for prompt"))
    dp.message.register(text_handler, F.text, StateFilter("waiting for prompt"))
    dp.message.register(voice_handler, F.voice, StateFilter("waiting for prompt"))


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())