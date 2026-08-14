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

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if not message.text or message.text.startswith('/'):
        return
    
    teks = message.text.lower()
    
    # 1. Topik Pokok Kelapa
    if any(k in teks for k in ["kelapa", "nyior", "santan"]):
        balasan = (
            "🥥 **Tips Penjagaan Pokok Kelapa Supaya Lebat Buah:**\n"
            "1. **Baja Unsur K (Kalium/Potash):** Pokok kelapa sangat memerlukan baja berkalium tinggi serta garam kasar di pangkal pokok untuk menguatkan buah.\n"
            "2. **Pembersihan Pelepah:** Buang pelepah tua yang melendut ke bawah agar pancaran cahaya matahari mengenai pucuk sepenuhnya.\n"
            "3. **Kawalan Perosak:** Awasi ancaman kumbang tanduk dan pastikan kawasan sekitar bersih."
        )
    # 2. Topik Pokok Pisang
    elif any(k in teks for k in ["pisang", "jantung"]):
        balasan = (
            "🍌 **Tips Penjagaan Pokok Pisang:**\n"
            "1. **Pangkas Anak:** Tinggalkan hanya 3 pokok sepokok (ibu, anak besar, cucu) supaya nutrien diserap sepenuhnya oleh buah.\n"
            "2. **Baja Buah:** Gunakan baja NPK 12-12-17 atau baja organik tahi ayam di sekeliling pangkal pokok secara berkala."
        )
    # 3. Topik Ayam: Sakit Mata
    elif any(k in teks for k in ["sakit mata", "mata", "bengkak mata"]):
        balasan = (
            "🩺 **Rawatan Mata Ayam Sakit:**\n"
            "1. Cuci mata ayam menggunakan air garam cair (suam kuku) atau ubat titik mata antiseptik (Terra-Cortril).\n"
            "2. Asingkan ayam yang sakit dari kawan-kawannya untuk elakkan jangkitan merebak."
        )
    # 4. Topik Ayam: Telur
    elif any(k in teks for k in ["telur", "bertelur", "penelur", "hasil"]):
        balasan = (
            "🥚 **Tips Supaya Ayam Rajin Bertelur:**\n"
            "1. Berikan dedak khusus penelur (*layer feed*) dicampur jagung hancur.\n"
            "2. Sediakan cahaya terang yang cukup dan sarang bertelur yang selesa serta gelap."
        )
    else:
        balasan = (
            f"🤖 Baik Wan, mengenai '{message.text}':\n\n"
            "Sebagai Doktor Unggas & Tanaman, saya sedia bantu! Cuba tanya tentang 'pokok kelapa', 'pokok pisang', 'ayam sakit mata', atau 'nak banyak telur'."
        )

    bot.reply_to(message, balasan)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
