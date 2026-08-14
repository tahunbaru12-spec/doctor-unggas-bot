import os
import telebot
from flask import Flask, request

TOKEN = "8740787222:AAHXoxcnFtN33LpieyEdFDLND9cHY1Z64Qo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

RENDER_URL = "https://doctor-unggas-bot.onrender.com/"

@app.route('/')
def home():
    return "Bot Doctor Unggas & Tanaman AI Aktif!"

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
    
    teks = message.text.lower()
    
    # 1. Topik Ayam: Sakit Mata
    if any(k in teks for k in ["sakit mata", "mata", "bengkak mata"]):
        balasan = (
            "🩺 **Rawatan Mata Ayam Sakit:**\n"
            "1. Cuci mata ayam menggunakan air garam cair (suam kuku) atau ubat titik mata antiseptik (seperti Terra-Cortril).\n"
            "2. Asingkan ayam yang sakit dari kawan-kawannya untuk elakkan jangkitan.\n"
            "3. Pastikan reban tidak berhabuk dan bebas daripada tahi bergas ammonia tinggi."
        )
    # 2. Topik Ayam: Telur
    elif any(k in teks for k in ["telur", "bertelur", "penelur", "hasil"]):
        balasan = (
            "🥚 **Tips Supaya Ayam Rajin & Banyak Bertelur:**\n"
            "1. **Makanan Berkualiti:** Berikan dedak khusus penelur (*layer feed*) dicampur jagung hancur.\n"
            "2. **Cahaya Cukup:** Ayam memerlukan sekurang-kurangnya 14 jam cahaya untuk merangsang hormon telur.\n"
            "3. **Vitamin & Kalsium:** Tambah serbuk kulit kerang atau vitamin penelur dalam air minuman.\n"
            "4. **Persekitaran Tenang:** Sediakan sarang bertelur yang gelap, selesa, bersih, dan bebas kutu."
        )
    # 3. Topik Tanaman: Pokok Pisang / Berbuah
    elif any(k in teks for k in ["pisang", "berbuah", "buah", "pokok"]):
        balasan = (
            "🍌 **Tips Penjagaan Pokok Pisang Supaya Lebat & Cepat Berbuah:**\n"
            "1. **Pangkas Anak Pokok:** Tinggalkan hanya 3 anak pokok sepokok (ibu, anak besar, dan cucu) supaya nutrien tidak berebut.\n"
            "2. **Baja Berkalium Tinggi:** Berikan baja organik atau baja buah (NPK 12-12-17 atau baja tahi ayam) secara berkala.\n"
            "3. **Pembersihan Pelepah:** Buang pelepah kering di bawah supaya pancaran matahari terkena penuh pada batang dan jantung.\n"
            "4. **Air Secukupnya:** Pastikan tanah lembap tetapi tidak bertakung air."
        )
    # 4. Topik Umum Makanan/Baja
    elif any(k in teks for k in ["makanan", "dedak", "makan", "pakan", "baja"]):
        balasan = (
            "🌱 **Panduan Umum Unggas & Tanaman:**\n"
            "• Bagi ternakan: Pastikan makanan bersih, kering, dan bernutrisi.\n"
            "• Bagi tanaman: Pastikan pencahayaan matahari mencukupi dan pembajaan dibuat mengikut jadual.\n"
            "• Ada soalan khusus tentang penyakit ayam atau tanaman tertentu? Boleh terus tanya!"
        )
    else:
        balasan = (
            f"🤖 Baik Wan, mengenai '{message.text}':\n\n"
            "Sebagai Doktor Unggas & Tanaman, saya sedia membantu! Coba tanyakan hal berkaitan 'penyakit ayam', 'nak banyak telur', atau 'cara lebatkan buah pisang'."
        )

    bot.reply_to(message, balasan)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
