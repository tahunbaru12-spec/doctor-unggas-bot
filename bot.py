import os
import telebot
from flask import Flask, request
import requests
import json

TOKEN = "8740787222:AAHXoxcnFtN33LpieyEdFDLND9cHY1Z64Qo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

RENDER_URL = "https://doctor-unggas-bot.onrender.com/"

# Token/Pin yang Wan berikan
USER_API_KEY = "AQ.Ab8RN6KnGgESJg0FtMIPy7sqrfgjvQlJrZuUwoh35UF7oiFGhQ"

@app.route('/')
def home():
    return "Bot Doctor Unggas & Tanaman Aktif!"

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
    
    # Respons pintar merangkumi semua jenis unggas (puyuh, ayam, itik) dan tanaman
    teks = message.text.lower()
    
    if any(k in teks for k in ["puyuh", "burung"]):
        balasan = (
            "🐦 **Panduan Penternakan Burung Puyuh:**\n"
            "1. **Makanan:** Berikan dedak pemula (*starter*) berprotein tinggi untuk anak puyuh dan dedak penelur untuk puyuh dewasa.\n"
            "2. **Suhu Reban:** Pastikan anak puyuh mendapat haba yang cukup pada minggu pertama.\n"
            "3. **Kebersihan:** Reban puyuh cepat berbau, jadi cuci alas dan kekalkan pengudaraan yang baik."
        )
    elif any(k in teks for k in ["ayam", "itik", "angsa"]):
        balasan = (
            "🐔 **Panduan Penternakan Unggas (Ayam/Itik):**\n"
            "1. Pastikan air minuman sentiasa bersih dan dicampur vitamin jika perlu.\n"
            "2. Kawal kebersihan reban untuk elakkan penyakit kutu, batuk, atau sakit mata.\n"
            "3. Berikan makanan seimbang mengikut peringkat umur ternakan."
        )
    elif any(k in teks for k in ["tanaman", "pokok", "sayur", "buah", "baja", "cili", "sawit", "getah"]):
        balasan = (
            "🌱 **Panduan Pertanian & Tanaman:**\n"
            "1. **Pencahayaan:** Pastikan pokok mendapat cahaya matahari secukupnya.\n"
            "2. **Pembajaan:** Gunakan baja yang bersesuaian (baja pertumbuhan atau baja buah/bunga).\n"
            "3. **Air & Saliran:** Pastikan tanah lembap tetapi air tidak bertakung di pangkal pokok untuk elakkan akar busuk."
        )
    else:
        balasan = (
            f"🤖 Baik Wan, mengenai '{message.text}':\n\n"
            "Sebagai Doktor Unggas & Tanaman, saya sedia bantu pelbagai jenis ternakan (ayam, itik, puyuh) dan tanaman (sayur, buah, pokok). Cuba tanya soalan yang lebih spesifik!"
        )

    bot.reply_to(message, balasan)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
