import os
import telebot
from flask import Flask
import threading

# Token baru yang telah di-reset
TOKEN = "8740787222:AAHXoxcnFtN33LpieyEdFDLND9cHY1Z64Qo"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Sedang Berjalan"

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Ujian sambungan: Bot akan membalas mesej Wan
    bot.reply_to(message, "Bot telah berjaya disambungkan! Mesej diterima: " + message.text)

def run_bot():
    try:
        bot.remove_webhook()
        bot.infinity_polling()
    except Exception as e:
        print(f"Error polling: {e}")

if __name__ == "__main__":
    # Menjalankan bot dalam thread berasingan supaya Flask boleh jalan serentak
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
