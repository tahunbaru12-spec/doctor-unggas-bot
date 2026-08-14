import os
import telebot
from flask import Flask, request
import google.generativeai as genai

# Token Telegram Bot Wan
TOKEN = "8740787222:AAHXoxcnFtN33LpieyEdFDLND9cHY1Z64Qo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

RENDER_URL = "https://doctor-unggas-bot.onrender.com/"

# Konfigurasi Google Gemini AI dengan PIN/API Key yang Wan berikan
GEMINI_API_KEY = "AQ.Ab8RN6KnGgESJg0FtMIPy7sqrfgjvQlJrZuUwoh35UF7oiFGhQ"
genai.configure(api_key=GEMINI_API_KEY)

# Tetapkan perwatakan bot sebagai Doktor Unggas & Tanaman yang pakar
generation_config = {
    "temperature": 0.7,
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Anda adalah 'Doktor Unggas & Tanaman', sebuah bot pakar pertanian, penternakan ayam, dan penjagaan tanaman di Malaysia. Jawab soalan pengguna dengan mesra, bernas, tepat, dan dalam bahasa Melayu yang mudah difahami."
)

@app.route('/')
def home():
    return "Bot Doctor Unggas & Tanaman AI Berkuasa Gemini Aktif!"

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
    
    try:
        # Hantar soalan Wan terus kepada AI Gemini
        response = model.generate_content(message.text)
        balasan = response.text
    except Exception as e:
        balasan = "Maaf Wan, sistem AI sedang sibuk sebentar. Cuba tanya sekali lagi ya!"

    bot.reply_to(message, balasan)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
