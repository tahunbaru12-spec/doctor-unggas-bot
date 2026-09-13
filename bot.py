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
GEMINI_API_KEY = "AQ.Ab8RN6IsGtHfk4rJN9JZr0kepqGVL7bMgFpIGz7SsDh0-Tw8fg"

@app.route(f'/{TOKEN}', methods=['POST'])
def receive_message():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(content_types=['photo', 'text', 'voice'])
def handle_all(message):
    try:
        system_instruction = "Anda adalah doktor pakar haiwan dan pertanian Malaysia. Bantu berikan diagnosis, nasihat, serta cari pautan atau maklumat laman web yang berkaitan jika diminta oleh pengguna secara mesra dan tepat."
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        headers = {
            'Content-Type': 'application/json',
            'x-goog-api-key': GEMINI_API_KEY
        }

        # 1. Jika Wan hantar gambar
        if message.content_type == 'photo':
            prompt = message.caption if message.caption else "Analisis gambar ini."
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            encoded_image = base64.b64encode(downloaded_file).decode('utf-8')
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"{system_instruction}. Analisis gambar ini dan jawab soalan ini: {prompt}"},
                            {"inline_data": {"mime_type": "image/jpeg", "data": encoded_image}}
                        ]
                    }
                ],
                "tools": [{"google_search": {}}]
            }

        # 2. Jika Wan hantar suara
        elif message.content_type == 'voice':
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            encoded_audio = base64.b64encode(downloaded_file).decode('utf-8')
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"{system_instruction}. Dengar mesej audio ini dan berikan jawapan."},
                            {"inline_data": {"mime_type": "audio/ogg", "data": encoded_audio}}
                        ]
                    }
                ],
                "tools": [{"google_search": {}}]
            }

        # 3. Jika teks biasa
        else:
            prompt = message.text
            if not prompt: prompt = "Berikan nasihat pakar."
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"{system_instruction}\n\nSoalan: {prompt}"}
                        ]
                    }
                ],
                "tools": [{"google_search": {}}]
            }

        response = requests.post(url, headers=headers, json=payload, timeout=60)
        data = response.json()
        
        if "candidates" in data:
            balasan = data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            balasan = f"Ralat API: {str(data)}"

        if len(balasan) > 4000:
            balasan = balasan[:4000] + "\n\n...(mesej dipendekkan)"
            
        bot.reply_to(message, balasan)
            
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
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
GEMINI_API_KEY = "AQ.Ab8RN6IsGtHfk4rJN9JZr0kepqGVL7bMgFpIGz7SsDh0-Tw8fg"

@app.route(f'/{TOKEN}', methods=['POST'])
def receive_message():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(content_types=['photo', 'text', 'voice'])
def handle_all(message):
    try:
        system_instruction = "Anda adalah doktor pakar haiwan dan pertanian Malaysia. Bantu berikan diagnosis, nasihat, serta cari pautan atau maklumat laman web yang berkaitan jika diminta oleh pengguna secara mesra dan tepat."
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        headers = {
            'Content-Type': 'application/json',
            'x-goog-api-key': GEMINI_API_KEY
        }

        # 1. Jika Wan hantar gambar
        if message.content_type == 'photo':
            prompt = message.caption if message.caption else "Analisis gambar ini."
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            encoded_image = base64.b64encode(downloaded_file).decode('utf-8')
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"{system_instruction}. Analisis gambar ini dan jawab soalan ini: {prompt}"},
                            {"inline_data": {"mime_type": "image/jpeg", "data": encoded_image}}
                        ]
                    }
                ],
                "tools": [{"google_search": {}}]
            }

        # 2. Jika Wan hantar suara
        elif message.content_type == 'voice':
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            encoded_audio = base64.b64encode(downloaded_file).decode('utf-8')
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"{system_instruction}. Dengar mesej audio ini dan berikan jawapan."},
                            {"inline_data": {"mime_type": "audio/ogg", "data": encoded_audio}}
                        ]
                    }
                ],
                "tools": [{"google_search": {}}]
            }

        # 3. Jika teks biasa
        else:
            prompt = message.text
            if not prompt: prompt = "Berikan nasihat pakar."
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"{system_instruction}\n\nSoalan: {prompt}"}
                        ]
                    }
                ],
                "tools": [{"google_search": {}}]
            }

        response = requests.post(url, headers=headers, json=payload, timeout=60)
        data = response.json()
        
        if "candidates" in data:
            balasan = data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            balasan = f"Ralat API: {str(data)}"

        if len(balasan) > 4000:
            balasan = balasan[:4000] + "\n\n...(mesej dipendekkan)"
            
        bot.reply_to(message, balasan)
            
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
