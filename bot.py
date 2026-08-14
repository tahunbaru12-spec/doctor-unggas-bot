import os
import telebot
from flask import Flask, request
import requests
import json

TOKEN = "8740787222:AAHXoxcnFtN33LpieyEdFDLND9cHY1Z64Qo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

RENDER_URL = "https://doctor-unggas-bot.onrender.com/"

@app.route('/')
def home():
    return "Bot Doctor Unggas & Tanaman AI Aktif!"

@app.route(f'/{TOKEN}', methods=['POST'])
def receive_message():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if not message.text or message.text.startswith('/'):
        return
    
    soalan_wan = message.text
    
    # Respons sementara yang lebih cerdik sementara sistem sambungan AI diaktifkan sepenuhnya
    balasan = (
        f"🤖 Wan, soalan mengenai: *\"{soalan_wan}\"*\n\n"
        "Saya sedang menaik taraf sistem supaya ia tidak lagi menggunakan senarai jawapan tetap, sebaliknya membolehkan AI menjawab secara automatik dan terperinci untuk sebarang jenis unggas (puyuh, ayam, itik) dan tanaman di dunia!"
    )

    bot.reply_to(message, balasan, parse_mode="Markdown")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
