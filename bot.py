import os
import telebot
from flask import Flask
import threading

TOKEN = "8740787222:AAHXoxcnFtN33LpieyEdFDLND9cHY1Z64Qo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Doctor Unggas Aktif!"

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

def run_polling():
    try:
        bot.remove_webhook()
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Polling error: {e}")

if __name__ == "__main__":
    # Jalankan polling dalam latar belakang
    threading.Thread(target=run_polling, daemon=True).start()
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
