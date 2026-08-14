import os
import telebot
from flask import Flask, request

TOKEN = "8740787222:AAHXoxcnFtN33LpieyEdFDLND9cHY1Z64Qo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

RENDER_URL = "https://doctor-unggas-bot.onrender.com/"

@app.route('/')
def home():
    return "Bot Doctor Unggas & Tanaman Aktif!"

@app.route(f'/{TOKEN}', methods=['POST'])
def receive_message():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@app.message_handler(func=lambda message: True)
def handle_message(message):
    if not message.text or message.text.startswith('/'):
        return
    
    teks = message.text.lower()
    
    # 1. Topik Ayam Sakit Kaki / Lumpuh
    if any(k in teks for k in ["sakit kaki", "lumpuh", "pincang", "bengkak kaki"]):
        balasan = (
            "🐔 **Rawatan Ayam Sakit Kaki / Pincang:**\n"
            "1. **Asingkan Reban:** Letakkan ayam di tempat beralas lembut (seperti jerami) supaya kakinya tidak terbeban.\n"
            "2. **Ubat & Vitamin:** Berikan vitamin B-Complex atau minyak ikan untuk menguatkan sendi dan saraf.\n"
            "3. **Periksa Tapak:** Lihat jika ada luka atau bengkak bernanah (*bumblefoot*). Cuci bersih jika ada luka."
        )
    # 2. Topik Burung Puyuh
    elif any(k in teks for k in ["puyuh", "burung"]):
        balasan = (
            "🐦 **Panduan Penternakan Burung Puyuh:**\n"
            "1. **Makanan:** Berikan dedak pemula (*starter*) berprotein tinggi untuk anak puyuh dan dedak penelur untuk puyuh dewasa.\n"
            "2. **Suhu & Lampu:** Pastikan anak puyuh mendapat haba yang cukup pada peringkat awal.\n"
            "3. **Kebersihan:** Cuci lantai reban kerap kerana najis puyuh cepat menghasilkan gas ammonia."
        )
    # 3. Topik Itik & Angsa
    elif any(k in teks for k in ["itik", "angsa", "mencit"]):
        balasan = (
            "🦆 **Panduan Penternakan Itik & Unggas Air:**\n"
            "1. **Air Minuman:** Pastikan air sentiasa ada kerana itik perlu basahkan paruh dan rongga hidung semasa makan.\n"
            "2. **Kawasan Mandi:** Sediakan bekas air yang cukup luas untuk mereka bersihkan diri.\n"
            "3. **Makanan:** Boleh campurkan dedak dengan dedak jagung atau sisa sayuran."
        )
    # 4. Topik Ayam secara umum / Sakit Mata
    elif any(k in teks for k in ["ayam", "sakit mata", "telur", "berak"]):
        balasan = (
            "🐓 **Panduan Kesihatan Ayam:**\n"
            "1. **Air & Vitamin:** Pastikan air minuman dicampur vitamin atau sedikit elektrolit.\n"
            "2. **Kawalan Penyakit:** Jika ada yang sakit mata, cuci dengan air garam suam kuku dan asingkan segera.\n"
            "3. **Makanan Seimbang:** Berikan dedak pencakar atau dedak penelur mengikut keperluan."
        )
    # 5. Topik Pelbagai Tanaman (Cili, Sayur, Buah, Sawit, Getah)
    elif any(k in teks for k in ["tanaman", "pokok", "sayur", "buah", "baja", "cili", "sawit", "getah", "mangga", "kelapa", "pisang"]):
        balasan = (
            "🌱 **Panduan Pertanian & Tanaman:**\n"
            "1. **Cahaya & Air:** Pastikan tanaman mendapat cahaya matahari penuh dan siraman air yang konsisten (tidak terlalu basah).\n"
            "2. **Pembajaan:** Gunakan baja tumbesaran (tinggi Nitrogen) untuk pokok muda, dan baja buah/bunga (tinggi Kalium & Fosforus) untuk pokok berbuah.\n"
            "3. **Kawalan Perosak:** Lakukan semburan cuka kayu atau racun organik jika diserang serangga perosak."
        )
    else:
        balasan = (
            f"🤖 Baik Wan, mengenai '{message.text}':\n\n"
            "Sebagai Doktor Unggas & Tanaman, saya boleh bantu jawab soalan berkaitan ayam, itik, burung puyuh, serta pelbagai jenis tanaman. Cuba tanyakan masalah yang lebih terperinci!"
        )

    bot.reply_to(message, balasan)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
