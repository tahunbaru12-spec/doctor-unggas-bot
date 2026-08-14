import os
import telebot
from flask import Flask, request

TOKEN = "8740787222:AAHXoxcnFtN33LpieyEdFDLND9cHY1Z64Qo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

RENDER_URL = "https://doctor-unggas-bot.onrender.com/"

@app.route('/')
def home():
    return "Bot Doctor Unggas Aktif!"

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
    
    teks = message.text.lower()
    if "sakit mata" in teks or "mata" in teks:
        balasan = "Bagi kes ayam sakit mata, cuci mata ayam dengan air garam cair atau ubat titik mata antiseptik, serta asingkan ayam yang sakit."
    elif "ayam" in teks:
        balasan = "Untuk kesihatan ayam, pastikan reban sentiasa kering, bersih, dan diberi makanan berkhasiat."
    else:
        balasan = f"Doktor Unggas terima mesej: '{message.text}'."

    bot.reply_to(message, balasan)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
