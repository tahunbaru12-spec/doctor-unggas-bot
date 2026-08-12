import os
import telebot
import requests
import threading
from flask import Flask

TELEGRAM_TOKEN = "8740787222:AAEL91UI9Qoatpo6DtViHD8yluyzCcHem1w"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Doctor Unggas & Tanaman aktif!"

def run_bot():
    try:
        bot.remove_webhook()
        print("Memulakan bot polling...")
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print(f"Ralat Polling: {e}")

@bot.message_handler(commands=["start", "stard", "help"])
def send_welcome(message):
    bot.reply_to(message, "Hai! Saya Doctor Unggas & Tanaman. Ada apa yang boleh saya bantu?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if not message.text or message.text.startswith('/'):
        return
    try:
        # Kita guna API percuma alternatif untuk respons
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        headers = {"Authorization": "Bearer hf_demo_token"} # Token awam percuma
        
        payload = {"inputs": f"Jawab dalam Bahasa Melayu ringkas untuk petani/penternak: {message.text}"}
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        
        res_json = response.json()
        if isinstance(res_json, list) and len(res_json) > 0:
            reply_text = res_json[0].get("generated_text", "Maaf, sistem sedang sibuk.")
            bot.reply_to(message, reply_text)
        else:
            bot.reply_to(message, "Ayam atau tanaman Wan sihat ke? Sila beritahu simptom dengan lebih jelas.")
    except Exception as e:
        bot.reply_to(message, "Sistem sedang berehat sekejap. Cuba hantar semula soalan.")

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
