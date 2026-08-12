import os
import telebot
from flask import Flask, request

TOKEN = "8740787222:AAHXoxcnFtN33LpieyEdFDLND9cHY1Z64Qo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# URL Render Wan
RENDER_URL = "https://doctor-unggas-bot.onrender.com/"

@app.route('/')
def home():
    return "Bot Webhook Aktif!"

@app.route(f'/{TOKEN}', methods=['POST'])
def receive_message():
    json_str = request.get_data().astype(str) if hasattr(request.get_data(), 'astype') else request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Bot Webhook berjaya terima: " + message.text)

if __name__ == "__main__":
    # Set webhook secara automatik semasa bot mula
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + TOKEN)
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
