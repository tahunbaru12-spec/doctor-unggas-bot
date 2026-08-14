import os
import telebot
import requests
import base64
from flask import Flask, request

TOKEN = "8740787222:AAHXoxcnFtN33LpieyEdFDLND9cHY1Z64Qo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

RENDER_URL = "https://doctor-unggas-bot.onrender.com/"
GROQ_API_KEY = "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"

# Simpan sejarah perbualan sementara untuk gambar terakhir
last_image_base64 = None

@app.route('/')
def home():
    return "Bot Groq Vision AI Sebenar Aktif!"

@app.route(f'/{TOKEN}', methods=['POST'])
def receive_message():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    global last_image_base64
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Tukar imej kepada format base64 supaya model Vision Groq boleh baca terus
        last_image_base64 = base64.b64encode(downloaded_file).decode('utf-8')
        
        kapsyen_pengguna = message.caption if message.caption else "Tolong analisis penyakit haiwan/tanaman dalam gambar ini dan berikan cadangan ubat yang spesifik."
        
        # Hantar imej dan soalan terus ke Groq Vision API
        balasan = hantar_vision_ke_groq(kapsyen_pengguna, last_image_base64)
    except Exception as e:
        balasan = f"Ralat memproses imej: {str(e)}"
        
    bot.reply_to(message, balasan)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    global last_image_base64
    if message.text.startswith('/'):
        return
    
    soalan_wan = message.text
    
    # Jika pengguna ada hantar gambar sebelum ni, sertakan sekali imej untuk dijawab oleh AI
    if last_image_base64:
        balasan = hantar_vision_ke_groq(soalan_wan, last_image_base64)
    else:
        balasan = hantar_teks_ke_groq(soalan_wan)
        
    bot.reply_to(message, balasan)

def hantar_vision_ke_groq(prompt_teks, img_base64):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.2-11b-vision-preview",
        "messages": [
            {
                "role": "system",
                "content": "Anda adalah Doktor Pakar Haiwan dan Pertanian Malaysia yang sangat arif merawat ayam, itik, lembu, kambing, arnab, dan tanaman. Berikan nama penyakit yang tepat serta senarai ubat/rawatan spesifik dalam bahasa Melayu secara mesra dan terperinci."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_teks
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_base64}"
                        }
                    }
                ]
            }
        ],
        "temperature": 0.4,
        "max_tokens": 1024
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Ralat pelayan Vision ({response.status_code}): Sila cuba sebentar lagi."
    except Exception as e:
        return f"Ralat sambungan Vision: {str(e)}"

def hantar_teks_ke_groq(prompt_teks):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "Anda adalah Doktor Pakar Haiwan dan Pertanian Malaysia. Jawab dalam bahasa Melayu."
            },
            {
                "role": "user",
                "content": prompt_teks
            }
        ]
    }
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=25
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "Maaf Wan, pelayan AI sedang sibuk."
    except Exception as e:
        return f"Ralat: {str(e)}"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
