import os

import telebot

from utils import analyse_url

BOT_TOKEN = '6297470757:AAGzjDQKD3itgi33BsjLu15RuWLMZf3sSYo'

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! PhishGuard orqali shubxali havolani tekshiring 👮‍♂️👀")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    sent_msg = bot.reply_to(message, "Iltimos, kutib turing...")
    text = analyse_url(message.text)
    sent_msg = bot.reply_to(message, text)

bot.infinity_polling()