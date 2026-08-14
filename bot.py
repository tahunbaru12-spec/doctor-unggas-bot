import os
import telebot
from flask import Flask, request
import requests

TOKEN = "8740787222:AAHXoxcnFtN33LpieyEdFDLND9cHY1Z64Qo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

RENDER_URL = "https://doctor-unggas-bot.onrender.com/"

# Kunci Direct AI Groq Wan
GROQ_API_KEY = "gsk_MCqDF8xo5IVP..."

@app.route('/')
def home():
    return "Bot Groq Direct AI Aktif!"

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
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "Anda adalah Doktor Pakar Haiwan, Ternakan, dan Pertanian Malaysia. Anda arif tentang ayam, itik, puyuh, lembu, kambing, dan semua jenis tanaman. Jawab soalan pengguna secara terus, terperinci, dan mesra dalam bahasa Melayu tanpa sebarang jawapan teks dalam kod."
            },
            {
                "role": "user",
                "content": soalan_wan
            }
        ]
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=20
        )
        
        if response.status_code == 200:
            hasil = response.json()
            balasan = hasil["choices"][0]["message"]["content"]
        else:
            balasan = "Maaf Wan, pelayan AI sedang sibuk. Cuba tanya sebentar lagi ya!"
    except Exception as e:
        balasan = f"Ralat sambungan AI: {str(e)}"

    bot.reply_to(message, balasan)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
