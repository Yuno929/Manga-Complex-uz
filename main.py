import os
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, filters

TOKEN = "8147212598:AAFoSF1Kz_1jd9qpmDcN60g0kN9ytCRuQG0"
bot = Bot(token=TOKEN)

app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

def handle_message(update, context):
    url = update.message.text
    chat_id = update.effective_chat.id

    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = url.split("/")[-1] or "file"
            with open(filename, "wb") as f:
                f.write(response.content)
            with open(filename, "rb") as f:
                context.bot.send_document(chat_id=chat_id, document=f)
        else:
            update.message.reply_text("Faylni yuklab bo‘lmadi.")
    except Exception as e:
        update.message.reply_text(f"Xatolik: {str(e)}")

from telegram.ext import CallbackContext
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route("/")
def index():
    return "Bot ishlayapti!", 200
