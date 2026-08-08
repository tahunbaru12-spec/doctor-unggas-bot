import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# Token bot dan API key
TELEGRAM_TOKEN = "8740787222:AAEL91UI9Qoatpo6DtViHD8yluyzCcHem1w"
GEMINI_API_KEY = "AQ.Ab8RN6JsJJlagi8qN8EQWBzd84nU4CYAYD4_iXVwAlnSDH0Log"

# Inisialisasi API Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot Doctor Unggas & Tanaman sedang aktif!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Hai! Saya Doctor Unggas & Tanaman yang dijana oleh AI Gemini. Ada apa yang boleh saya bantu berkaitan ayam, burung, atau tanaman hari ini?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Maaf, berlaku ralat sedikit. Cuba lagi nanti.")

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    
    print("Bot sedang berjalan...")
    bot.infinity_polling()
