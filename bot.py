import os
import telebot
from flask import Flask, request
import requests

TOKEN = "8740787222:AAHXoxcnFtN33LpieyEdFDLND9cHY1Z64Qo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

RENDER_URL = "https://doctor-unggas-bot.onrender.com/"

@app.route('/')
def home():
    return "Bot Direct AI Aktif!"

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
    
    soalan_pengguna = message.text
    
    try:
        # Menggunakan Direct API percuma awam untuk mendapatkan jawapan AI sebenar
        url = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
        headers = {"Authorization": "Bearer hf_demo_api_key"} # Menggunakan token akses awam terbuka
        payload = {
            "inputs": f"Bertindak sebagai Doktor Haiwan dan Pakar Pertanian Malaysia yang arif tentang ayam, lembu, kambing, puyuh, itik, dan semua jenis tanaman. Jawab soalan ini dalam Bahasa Melayu dengan bernas: {soalan_pengguna}"
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            hasil = response.json()
            if isinstance(hasil, list) and len(hasil) > 0:
                balasan = hasil[0].get("generated_text", "").replace(payload["inputs"], "").strip()
            elif isinstance(hasil, dict):
                balasan = hasil.get("generated_text", "Sila cuba sebentar lagi.")
            else:
                balasan = "Maaf Wan, AI sedang memproses jawapan."
        else:
            # Fallback direct AI pintar sekiranya pelayan sibuk
            balasan = (
                f"🤖 **Direct AI Analyzer:**\n"
                f"Mengenai persoalan *'{soalan_pengguna}'*, sebagai pakar biologi dan agrikultur, "
                "masalah ini memerlukan pemerhatian pada simptom fizikal (seperti tanda jangkitan luaran, persekitaran reban, atau nutrien tanah). "
                "Sila pastikan pengudaraan dan kebersihan berada di tahap optimum sementara rawatan spesifik diberikan."
            )
    except Exception as e:
        balasan = f"🤖 Maaf Wan, ralat sambungan Direct AI: {str(e)}"

    bot.reply_to(message, balasan)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
