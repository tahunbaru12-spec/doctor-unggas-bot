import os
import telebot
from flask import Flask, request
import requests

ADMIN_USER_ID = 8719826950
TARGET_CHAT_ID = -1003572908909

TOKEN = "8740787222:AAHXoxcnFtN33LpieyEdFDLND9cHY1Z64Qo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

RENDER_URL = "https://doctor-unggas-bot.onrender.com/"
GROQ_API_KEY = "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"

@app.route(f'/{TOKEN}', methods=['POST'])
def receive_message():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(content_types=['photo', 'text', 'voice'])
def handle_all(message):
    try:
        system_prompt = "Anda doktor pakar haiwan dan pertanian Malaysia. Berikan jawapan tepat, lengkap, dan rujuk maklumat semasa dari web jika perlu."
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}", 
            "Content-Type": "application/json"
        }
        
        user_text = message.text if message.text else message.caption
        if not user_text:
            user_text = "Berikan nasihat pakar pertanian/haiwan."

        if message.content_type == 'photo':
            user_text = f"Pengguna menghantar gambar dengan soalan: {user_text}. Sila buat carian web jika perlu untuk memberi maklumat rawatan tepat."

        # Menggunakan model compound Groq yang mempunyai keupayaan carian web terbina dalam
        payload = {
            "model": "groq/compound",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            "tools": [{"type": "web_search"}],
            "max_tokens": 1000
        }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=60)
        data = response.json()
        
        if "choices" in data:
            balasan = data["choices"][0]["message"]["content"]
        else:
            balasan = f"Ralat: {str(data)}"
            
        bot.reply_to(message, balasan)
            
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
