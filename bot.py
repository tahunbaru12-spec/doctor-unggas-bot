import os
import telebot
from flask import Flask
import threading

TOKEN = "8740787222:AAEL91UI9Qoatpo6DtViHD8yluyzCcHem1w"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Sedang Berjalan"

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Bot akan membalas dengan teks yang sama untuk test sambungan
    bot.reply_to(message, "Bot sedang aktif! Saya terima mesej anda: " + message.text)

def run_bot():
    bot.remove_webhook()
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
