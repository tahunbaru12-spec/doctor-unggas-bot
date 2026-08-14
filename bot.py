import os
import telebot
from flask import Flask, request

TOKEN = "8740787222:AAHXoxcnFtN33LpieyEdFDLND9cHY1Z64Qo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

RENDER_URL = "https://doctor-unggas-bot.onrender.com/"

@app.route('/')
def home():
    return "Bot Doctor Pakar Aktif!"

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
    
    soalan = message.text.lower()
    
    # Respons automatik universal yang profesional
    if any(k in soalan for k in ["sakit", "rawatan", "ubat", "penyakit"]):
        balasan = (
            f"🩺 **Panduan Rawatan & Kesihatan:**\n"
            f"Mengenai masalah *'{message.text}'*:\n"
            "1. **Asingkan Ternakan:** Pastikan haiwan yang sakit diasingkan segera dari yang sihat bagi mengelakkan jangkitan.\n"
            "2. **Kebersihan & Nutrisi:** Berikan air bersih yang dicampur vitamin/elektrolit serta pastikan reban kering dan selesa.\n"
            "3. **Rujukan Spesifik:** Jika berlarutan, rujuk simptom khusus seperti cirit-birit, bengkak, atau luka untuk rawatan ubat yang tepat."
        )
    elif any(k in soalan for k in ["tanaman", "pokok", "baja", "buah", "sayur", "daun"]):
        balasan = (
            f"🌱 **Panduan Pertanian & Tanaman:**\n"
            f"Mengenai *'{message.text}'*:\n"
            "1. **Cahaya & Air:** Pastikan tanaman mendapat pancaran matahari yang cukup dan pengaliran air yang baik (tidak bertakung).\n"
            "2. **Pembajaan:** Gunakan baja yang mengikut peringkat umur pokok (baja pertumbuhan atau baja buah).\n"
            "3. **Kawalan Perosak:** Periksa bahagian daun atau akar jika ada tanda serangan serangga atau kulat."
        )
    else:
        balasan = (
            f"🤖 Baik Wan, mengenai soalan *'{message.text}'*:\n\n"
            "Sebagai Doktor Unggas, Ternakan & Tanaman, saya bersedia membantu anda. Sila ajukan pertanyaan yang lebih spesifik mengenai ayam, itik, puyuh, lembu, kambing, atau apa jua jenis tanaman!"
        )

    bot.reply_to(message, balasan)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
