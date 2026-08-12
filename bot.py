import os
import telebot
from google import genai
import threading
from flask import Flask

TELEGRAM_TOKEN = "8740787222:AAEL91UI9Qoatpo6DtViHD8yluyzCcHem1w"
GEMINI_API_KEY = "AQ.Ab8RN6JR4VrGLzBJ_biJVGZISoclTYRFSUALRMHNL0CnxZxJxA"

client = genai.Client(api_key=GEMINI_API_KEY)
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
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Ralat AI: {str(e)}")

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
