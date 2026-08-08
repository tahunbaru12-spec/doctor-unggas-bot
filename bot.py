import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

genai.configure(api_key="MASUKKAN_GEMINI_API_KEY_DI_SINI")
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    prompt = f"Anda adalah pakar AI kesihatan unggas dan penjagaan tanaman. Jawab soalan ini dengan mesra dan profesional: {user_message}"
    
    response = model.generate_content(prompt)
    await update.message.reply_text(response.text)

if __name__ == '__main__':
    TOKEN = "8740787222:AAEL91UI9Qoatpo6DtViHD8yluyzCcHem1w"
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot AI sedang berjalan...")
    app.run_polling()

