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
	start_markup.row('/start', '/help', '/hide')
	start_markup.row('/weather', '/world_time', '/news')
	start_markup.row('/crypto', '/stocks', '/translate')
	bot.send_message(message.chat.id, "🤖 The bot has started!\n⚙ Enter /help to see bot's function's")
	bot.send_message(message.from_user.id, "⌨️ The Keyboard is added!\n⌨️ /hide To remove kb ", reply_markup=start_markup)

@bot.message_handler(commands=['hide'])
def command_hide(message):
	hide_markup = telebot.types.ReplyKeyboardRemove()
	bot.send_message(message.chat.id, "⌨💤...", reply_markup=hide_markup)


@bot.message_handler(commands=['help'])
def command_help(message):
	bot.send_message(message.chat.id, "🤖 /start - display the keyboard\n"
									  "☁ /weather - current forecast\n"
									  "💎 /crypto - current cryptocurrency\n"
									  "⌛️ /world_time - current time\n"
									  "📊 /stocks - current stocks prices\n"
									  "📰 /news - latest bbc article\n"
									  "🔁 /translate - language translator")
"""
@bot.message_handler(commands=['weather'])
def command_weather(message):
	sent = bot.send_message(message.chat.id, "🗺 Enter the City or Country\n🔍 In such format:  Toronto  or  japan")
	bot.register_next_step_handler(sent, send_forecast)
"""
"""
def send_forecast(message):
	try:
		get_forecast(message.text)
	except pyowm.exceptions.api_response_error.NotFoundError:
		bot.send_message(message.chat.id, "❌  Wrong place, check mistakes and try again!")
	forecast = get_forecast(message.text)
	bot.send_message(message.chat.id, forecast)
"""

@bot.message_handler(commands=['world_time'])
def command_world_time(message):
	sent = bot.send_message(message.chat.id, "🗺 Enter the City or Country\n🔍 In such format:  Moscow  or  china")
	bot.register_next_step_handler(sent, send_time)

def get_time(place):
	page = requests.get('https://www.google.com/search?client=firefox-b-d&q=time+in+'+place)
	soup = BeautifulSoup(page.text, "html.parser")
	parsed_time = soup.find_all('div', {'class': 'BNeawe iBp4i AP7Wnd'})[1].find_all(text=True, recursive=True)
	time = f'⏰ In {place} is {parsed_time[0]}'
	return time

def send_time(message):
	try:
		get_time(message.text)
	except IndexError:
		bot.send_message(message.chat.id, "❌ Wrong place, check mistakes and try again")
	time = get_time(message.text)
	bot.send_message(message.chat.id, time)


@bot.message_handler(commands=['news'])
def get_article():
    bbc_request = requests.get('https://www.bbc.com/news')
    soup = BeautifulSoup(bbc_request.text, "html.parser")
    raw_article = soup.find_all('div', {'class': 'gs-c-promo-body gel-1/2@xs gel-1/1@m gs-u-mt@m'})[0].find_all(text=True, recursive=True)
    if raw_article[0].startswith('Video'): #Cheking if article has video and then moving index by 1 for proper display in message
        topic = raw_article[5]
        title = raw_article[1]
        description = raw_article[2]
        publish_time = raw_article[4]
    else:
        topic = raw_article[4]
        title = raw_article[0]
        description = raw_article[1]
        publish_time = raw_article[3]
    href = soup.find_all('div', {'class': 'gs-c-promo-body gel-1/2@xs gel-1/1@m gs-u-mt@m'})[0].find('a', {'class': 'gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor'})['href']
    link = f' https://www.bbc.com{href}'
    article = f'✏️ <b>Topic</b>:  {topic}\n⚠️ <b>Title</b>:  {title}\n📌 <b>Description</b>:  {description}\n🕒 <b>Published</b>:  {publish_time}\n➡️ <b>Full article</b>: {link}'
    return article

def command_news(message):
	bot.send_message(message.chat.id, "🆕 Latest BBC article:\n")
	bot.send_message(message.chat.id, get_article(), parse_mode='HTML')



while True:
	try:
		bot.polling()
	except Exception:
		tm.sleep(1)