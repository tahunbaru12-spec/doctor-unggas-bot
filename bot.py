import os
import telebot
from flask import Flask, request
import requests
import base64

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
        
        # Jika pengguna hantar gambar
        if message.content_type == 'photo':
            # Ambil gambar kualiti tertinggi
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            encoded_image = base64.b64encode(downloaded_file).decode('utf-8')
            
            payload = {
                "model": "llama-3.2-11b-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"Anda doktor pakar haiwan dan pertanian Malaysia. Analisis gambar ini dan jawab mesej ini: {prompt}"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                        ]
                    }
                ],
                "max_tokens": 1000
            }
        else:
            # Jika pengguna hantar teks biasa
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "user", 
                        "content": f"Anda doktor pakar haiwan dan pertanian Malaysia. Jika ditanya tentang pembekal atau tempat beli, berikan panduan umum cara mencari atau senaraikan platform lazim di Malaysia. Jawab secara ringkas dan padat: {prompt}"
                    }
                ]
            }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=45)
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
