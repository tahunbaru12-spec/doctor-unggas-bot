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
    
    # Jawapan bijak dan terperinci untuk pelbagai situasi ayam & tanaman
    if "sakit mata" in teks or "mata" in teks:
        balasan = (
            "🩺 **Rawatan Mata Ayam Sakit:**\n"
            "1. Cuci mata ayam menggunakan air garam cair (suam kuku) atau ubat titik mata antiseptik (seperti Terra-Cortril).\n"
            "2. Asingkan ayam yang sakit dari kawan-kawannya untuk elakkan jangkitan.\n"
            "3. Pastikan reban tidak berhabuk dan bebas daripada tahi yang bergas ammonia tinggi."
        )
    elif "kurang bertelur" in teks or "tak bertelur" in teks:
        balasan = (
            "🥚 **Tips Tingkatkan Hasil Telur Ayam:**\n"
            "1. **Makanan Berkhasiat:** Berikan dedak penelur (*layer feed*) yang tinggi kalsium dan protein.\n"
            "2. **Cahaya Cukup:** Ayam butuh sekurang-kurangnya 14 jam cahaya sehari untuk merangsang pengeluaran telur.\n"
            "3. **Kesihatan & Vitamin:** Berikan tambahan vitamin B-Complex atau serbuk kulit kerang dalam makanan.\n"
            "4. **Kurangkan Stres:** Pastikan reban tenang, tidak diganggu pemangsa, dan bebas kutu."
        )
    elif "rajin bertelur" in teks or "banyak telur" in teks:
        balasan = (
            "🌟 **Cara Kekalkan Ayam Rajin Bertelur:**\n"
            "• Beri dedak khusus penelur campuran jagung hancur.\n"
            "• Sediakan air bersih secukupnya setiap hari (tambah vitamin penelur jika ada).\n"
            "• Sediakan sarang bertelur yang gelap, selesa, dan bersih agar ayam selesa bertelur di tempatnya."
        )
    elif "makanan" in teks or "dedak" in teks:
        balasan = (
            "🌽 **Panduan Pemakanan Unggas:**\n"
            "• Anak ayam (Starter): Dedak tinggi protein (1-4 minggu).\n"
            "• Ayam dewasa/penelur: Campuran dedak penelur, jagung hancur, dan dedak padi secukupnya.\n"
            "• Pastikan bekas makanan sentiasa kering dan tiada kulat."
        )
    else:
        balasan = (
            f"🤖 Soalan bagus: '{message.text}'\n\n"
            "Sebagai Doktor Unggas & Tanaman, saya sarankan agar pemakanan, kebersihan reban, dan vaksinasi dijaga rapi. "
            "Ada apa-apa masalah spesifik mengenai penyakit ayam atau tanaman yang Wan ingin tanyakan lagi?"
        )

    bot.reply_to(message, balasan)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
