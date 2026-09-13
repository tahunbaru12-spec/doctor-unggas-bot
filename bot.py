import os
import telebot
from flask import Flask, request
from google import genai
from google.genai import types

ADMIN_USER_ID = 8719826950
TARGET_CHAT_ID = -1003572908909

TOKEN = "8740787222:AAHXoxcnFtN33LpieyEdFDLND9cHY1Z64Qo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

RENDER_URL = "https://doctor-unggas-bot.onrender.com/"

# Kunci API Gemini Wan dimasukkan di sini
GEMINI_API_KEY = "AQ.Ab8RN6IsGtHfk4rJN9JZr0kepqGVL7bMgFpIGz7SsDh0-Tw8fg"
client = genai.Client(api_key=GEMINI_API_KEY)

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
        
        # 1. Jika Wan hantar mesej suara (Voice Note)
        if message.content_type == 'voice':
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    types.Part.from_bytes(
                        data=downloaded_file,
                        mime_type='audio/ogg',
                    ),
                    "Dengar mesej suara ini dan bertindak sebagai doktor pakar haiwan dan pertanian Malaysia untuk berikan jawapan."
                ],
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=[{"google_search": {}}]
                )
            )
            balasan = response.text

        # 2. Jika Wan hantar gambar
        elif message.content_type == 'photo':
            prompt = message.caption if message.caption else "Analisis gambar ini."
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    types.Part.from_bytes(
                        data=downloaded_file,
                        mime_type='image/jpeg',
                    ),
                    f"Bertindak sebagai doktor pakar haiwan dan pertanian Malaysia. Analisis gambar ini dan jawab soalan ini: {prompt}"
                ],
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=[{"google_search": {}}]
                )
            )
            balasan = response.text

        # 3. Jika Wan hantar teks biasa
        else:
            prompt = message.text
            if not prompt: prompt = "Berikan nasihat pakar."
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=[{"google_search": {}}]
                )
            )
            balasan = response.text

        if len(balasan) > 4000:
            balasan = balasan[:4000] + "\n\n...(mesej dipendekkan)"
            
        bot.reply_to(message, balasan)
            
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
