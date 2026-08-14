import os
import telebot
from flask import Flask, request
import requests
import base64
from PIL import Image
import io

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

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Dapatkan fail gambar paling jelas
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Kecilkan saiz gambar (resize) supaya tidak kena ralat saiz
        img = Image.open(io.BytesIO(downloaded_file))
        img.thumbnail((800, 800)) # Hadkan saiz supaya selamat
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        prompt = message.caption if message.caption else "Analisis penyakit haiwan dalam gambar ini dan berikan ubat."

        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.2-11b-vision-preview",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Anda doktor pakar haiwan. Berdasarkan gambar: {prompt}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                ]
            }]
        }
        
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        balasan = response.json()["choices"][0]["message"]["content"]
        bot.reply_to(message, balasan)
        
    except Exception as e:
        bot.reply_to(message, f"Ralat AI Vision: {str(e)}")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
