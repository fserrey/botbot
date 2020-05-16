#Un bot que devuelve el significado de una palabra

import telebot
from telebot import types
import re
import time as tm
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
load_dotenv()

#os.environ.get('BOT_TOKEN')
bot_key = os.environ["TOKEN_MITH"]

bot = telebot.TeleBot(bot_key, threaded=False)

@bot.message_handler(commands=['start'])
def command_start(message):
	start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	start_markup.row('/start', '/help')
	start_markup.row('/buscar', '/ilústrame')
	bot.send_message(message.chat.id, "🤖 ¡Hola, soy el nuevo becario de la RAE!\n⚙ Escribe /buscar y te cuento cómo resolver tus dudas lingüísticas\n")

@bot.message_handler(commands=['help'])
def command_help(message):
	bot.send_message(message.chat.id, "🤖 /start - Menú principal\n"
									  "📰 /ilústrame - Tu pildorita cultural diaria\n"
									  "🔁 /buscar - Resuelve tus dudas lingüísticas")

@bot.message_handler(commands=['buscar'])
def command_world_time(message):
	sent = bot.send_message(message.chat.id, "🔍 ¿Qué palabra te gustaría buscar?\n")
	bot.register_next_step_handler(sent, send_definition)

def get_palabra(termino):
	try:
		page = requests.get('https://dle.rae.es/' + termino.lower())
		soup = BeautifulSoup(page.text, "html.parser")
		parsed_definition = soup.article.text
		definition = f'La RAE define {termino} como:\n {parsed_definition}'
		return definition
	
	except len(definition) < len(termino):
		return f'🤖 Error 404: {termino} not found\n ¿Hablas español?'


def send_definition(message):
	try:
		get_palabra(message.text)
	except IndexError:
		bot.send_message(message.chat.id, "❌ Ups, algo ha ido mal, prueba de nuevo")
	definition = get_palabra(message.text)
	bot.send_message(message.chat.id, definition)

#@bot.message_handler(commands=['ilústrame'])
#bot.send_message(chat_id=chat_id, text="")



while True:
	try:
		bot.polling()
	except Exception:
		tm.sleep(1)