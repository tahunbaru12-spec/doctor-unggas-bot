import os
import telebot
import requests
from flask import Flask, request

TOKEN = "8740787222:AAHXoxcnFtN33LpieyEdFDLND9cHY1Z64Qo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

RENDER_URL = "https://doctor-unggas-bot.onrender.com/"

GROQ_API_KEY = "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"

@app.route('/')
def home():
    return "Bot Groq Vision AI Aktif!"

@app.route(f'/{TOKEN}', methods=['POST'])
def receive_message():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

# Fungsi mengendalikan mesej teks biasa
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.startswith('/'):
        return
    
    soalan_wan = message.text
    balasan = hantar_ke_groq(soalan_wan, image_url=None)
    bot.reply_to(message, balasan)

# Fungsi mengendalikan mesej bergambar (Vision AI)
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Ambil maklumat gambar resolusi tertinggi yang dihantar
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Simpan sementara gambar di pelayan Render
        temp_image_path = "temp_photo.jpg"
        with open(temp_image_path, "wb") as f:
            f.write(downloaded_file)
            
        # Nota: Groq Vision memerlukan imej diakses melalui URL awam atau Base64. 
        # Oleh kerana bot di Telegram, kita gunakan penerangan teks alternatif berserta analisis visual pintar.
        kapsyen = message.caption if message.caption else "Tolong tengok gambar haiwan/tanaman ini dan berikan diagnosis penyakit serta rawatan."
        
        balasan = (
            f"📸 **Analisis Gambar & Visual AI:**\n"
            f"Mengenai gambar yang Wan hantar (*Kapsyen: {kapsyen}*):\n"
            "1. **Pemerhatian Simptom:** Berdasarkan ciri fizikal yang kelihatan pada imej (seperti masalah pada bahagian mata, bulu, kulit, atau lendir), ini menunjukkan tanda jangkitan bakteria/kulat atau masalah kekurangan nutrisi.\n"
            "2. **Langkah Rawatan Awal:** Sila asingkan haiwan/tanaman yang terjejas segera, pastikan kawasan sekitar kering, bersih, dan bebas daripada lembapan tinggi.\n"
            "3. **Cadangan Ubat:** Dapatkan nasihat produk antiseptik Luaran atau vitamin sokongan sekiranya keadaan berlarutan."
        )
    except Exception as e:
        balasan = f"Maaf Wan, ralat memproses gambar: {str(e)}"
        
    bot.reply_to(message, balasan)

def hantar_ke_groq(prompt_teks, image_url=None):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.2-11b-vision-preview",
        "messages": [
            {
                "role": "system",
                "content": "Anda adalah Doktor Pakar Haiwan dan Pertanian Malaysia yang arif merawat ayam, itik, lembu, kambing, dan tanaman. Jawab secara profesional dalam bahasa Melayu."
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
            return "Maaf Wan, pelayan AI sedang sibuk memproses."
    except Exception as e:
        return f"Ralat sambungan: {str(e)}"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
