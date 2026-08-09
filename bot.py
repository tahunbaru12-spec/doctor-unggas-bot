import os
import telebot
from google import genai
from flask import Flask, request

TELEGRAM_TOKEN = "8740787222:AAEL91UI9Qoatpo6DtViHD8yluyzCcHem1w"
GEMINI_API_KEY = "AQ.Ab8RN6JsJJlagi8qN8EQWBzd84nU4CYAYD4_iXVwAlnSDH0Log"

client = genai.Client(api_key=GEMINI_API_KEY)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Doctor Unggas & Tanaman aktif!"

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def receive_message():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    return "Invalid Request", 403

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
    bot.remove_webhook()
    bot.set_webhook(url=f"https://doctor-unggas-bot.onrender.com/{TELEGRAM_TOKEN}")
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
