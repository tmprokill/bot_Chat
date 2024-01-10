import asyncio
from helpers.database_connector import SQLiteConnector
import logging
import ast
from openai import OpenAI
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton 
import re
#openAI

client = OpenAI(api_key="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")
logging.basicConfig(level=logging.INFO)

#database
db = SQLiteConnector("database\\users.db")


#unicode flags
britain = u"\U0001F1EC\U0001F1E7"
ukraine = u"\U0001F1FA\U0001F1E6"
#Classes
#File class that is being used to distrubute voice messages
class File:
    free = True
    def isFree(self):
        return self.free
    
    def switch(self):
        if self.free == True: 
            self.free = False
        else:
            self.free = True


#Functions
#telegram keyboards
def initialize_languages():
    button_language_eng = KeyboardButton(text=f"{britain}")
    button_language_ua = KeyboardButton(text=f"{ukraine}")
    return ReplyKeyboardMarkup(keyboard=[[button_language_eng], [button_language_ua]], resize_keyboard=True, one_time_keyboard=True)


#getting the language from db
def get_language(id):
    value = db.fetch_data_one("SELECT language FROM users WHERE id = ?", (id,))
    return value[0]
          
            
#Saving chat history (all the messages)
def save_chat(text, role, id):
    user = 'user' if role == 1 else 'assistant'
    text = str({'role': f'{user}', 'content': f"{text}"}) + "\n" + "#123#"
    db.execute_query("UPDATE users SET chat = chat || ? WHERE id = ?", (text, id))            


#Function which makes the answer and saves it to the database
def ask_and_save(user_request, id):
    save_chat(user_request, 1, id)
    reply = ask_chat(id)
    save_chat(reply, 2, id)
    return reply


#dispense the files to load audio-data
def dispenser(farr: list[File]):
    for i, item in enumerate(farr):
        if item.free == True:
            filename = f"voice\\file_{str(i)}.mp3"
            item.switch()
            return [i, filename]
    return False


#Voice message Downloader
async def downloader(bot: Bot, filearray: list,  message: types.Message) -> list:
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    
    checkFree = dispenser(filearray)
    if checkFree != False:
        await bot.download_file(file_path, checkFree[1])
        return checkFree
    else:
        while checkFree == False:
            await asyncio.sleep(15)
            checkFree = dispenser(filearray)
    await bot.download_file(file_path, checkFree[1])
    return checkFree


#Truncate the beginning of the chat if it overflows the usage tokens
def truncate_chat(haystack: str, needle: str, n: int) -> int:
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    result = haystack[start+5:]
    return result


#OpenAI functions
def transcipt_file(audio_file):    
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="text"
    )
    return transcript

#ChatGPT prompt and parsing answer
def ask_chat(id):
    #getting data in an array of dictionaries
    messages = []
    request_db = "".join(db.fetch_data_one("SELECT chat FROM users WHERE id = ?", (id,))).split('#123#')
    request_db.pop()
    for item in request_db:
        messages.append(ast.literal_eval(item))
    response = client.chat.completions.create(model='gpt-3.5-turbo', messages=messages)
    #checking for tokens used
    usage = response.usage.total_tokens
    if usage >= 3500:
        chat = db.fetch_data_one("SELECT chat FROM users WHERE id = ?", (id,))[0]
        db.execute_query("UPDATE users SET chat = ? WHERE id = ?", (truncate_chat(chat, "#123#", 4),id))
    result = response.choices[0].message.content
    result = add_extra_backslash(result)
    return result


#escaping special symbols for MarkdownV2
def add_extra_backslash(text):
    special_characters = r'[.\-/~>=*#+?!^${}()|\[\]\\]'
    replaced_text = re.sub(special_characters, r'\\\g<0>', text)
    return replaced_text


