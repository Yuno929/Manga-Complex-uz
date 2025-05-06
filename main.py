main.py
import telebot
import requests
import os

TOKEN = "8147212598:AAFoSF1Kz_1jd9qpmDcN60g0kN9ytCRuQG0"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Menga faylning silkasini yuboring.")

@bot.message_handler(func=lambda message: message.text.startswith("http"))
def download(message):
    url = message.text
    try:
        response = requests.get(url)
        filename = url.split("/")[-1]
        with open(filename, 'wb') as f:
            f.write(response.content)
        with open(filename, 'rb') as f:
            bot.send_document(message.chat.id, f)
        os.remove(filename)
    except:
        bot.reply_to(message, "Xatolik yuz berdi. Silka noto‘g‘ri bo‘lishi mumkin.")

bot.polling()