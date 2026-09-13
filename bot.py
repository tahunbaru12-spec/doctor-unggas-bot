import os
import telebot
from flask import Flask, request
import requests
import base64
from PIL import Image
import io

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

@bot.message_handler(content_types=['photo', 'text'])
def handle_all(message):
    try:
        prompt = message.caption if message.caption else message.text
        if not prompt: prompt = "Berikan nasihat pakar."

        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        
        if message.content_type == 'photo':
            text_prompt = f"Pengguna menghantar gambar dengan mesej: {prompt}. Bertindaklah sebagai doktor pakar haiwan dan pertanian Malaysia untuk berikan diagnosis dan ubat yang tepat."
        else:
            text_prompt = f"Anda doktor pakar haiwan dan pertanian Malaysia. Jawab soalan ini secara ringkas, padat, dan terperinci: {prompt}"

        payload = {
            "model": "openai/gpt-oss-20b",
            "messages": [{"role": "user", "content": text_prompt}]
        }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=30)
        data = response.json()
        
        if "choices" in data:
            balasan = data["choices"][0]["message"]["content"]
            if len(balasan) > 4000:
                balasan = balasan[:4000] + "\n\n...(mesej dipendekkan)"
            bot.reply_to(message, balasan)
        else:
            bot.reply_to(message, f"Ralat: {str(data)}")
            
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
