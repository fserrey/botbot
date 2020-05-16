import telebot
from telebot import types
import re
import os
from dotenv import load_dotenv
load_dotenv()

#os.environ.get('BOT_TOKEN')
bot_key = os.environ["TOKEN"]

locale.setlocale(locale.LC_ALL, 'es_ES.utf8')

# Get bot token from environment variable BOT_TOKEN
bot = telebot.TeleBot(bot_key, threaded=False)


@bot.message_handler(commands=['start'])
def welcome_message(message):
    msg = """¡Bienvenid@ humano! 
    Este es un bot experimental. Por lo que es posible que experimentes cosas inesperadas 🤖"""

    log_command(message)
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['help'])
def help_message(message):
    msg = "Mensaje de ayuda"
    log_command(message)
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['bulos', 'actualidad', 'tiempo'])
def send_menu(message):
    # Parse command correctly (avoid content after @)
    regex = re.compile('\/\w*')
    command = regex.search(message.text).group(0)
    log_command(message)
    send_menu_image(message.chat.id, command.replace("/", ""))

@bot.message_handler(commands=['opciones', 'help'])
def send_opciones(message):
    '''
    Display the commands and what are they intended for.
    '''
    bot.reply_to(message, build_help_message())
    markup = types.ReplyKeyboardMarkup()
    item_dondehoy = types.KeyboardButton('/dondehoy')
    item_dondeproximamente = types.KeyboardButton('/dondeproximamente')
    item_hedonadohoy = types.KeyboardButton('/hedonadohoy')
    item_puedodonar = types.KeyboardButton('/puedodonar')
    markup.row(item_dondehoy, item_dondeproximamente)
    markup.row(item_hedonadohoy, item_puedodonar)
    bot.send_message(message.chat.id, "\n\nPara continuar escribe un comando o seleccionalo directamente del menu inferior.", reply_markup=markup)
