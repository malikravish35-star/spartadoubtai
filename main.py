import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- 1. RENDER PORT BINDING (FLASK) ---
app = Flask('')

@app.route('/')
def home():
    return "Sparta Bot is Online!"

def run():
    # Render port 8080 use karta hai
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. AI & BOT CONFIGURATION ---
TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_KEY')

genai.configure(api_key=GEMINI_KEY)

# 404 Error fix karne ke liye full model path
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
bot = telebot.TeleBot(TOKEN)

# --- 3. WELCOME MESSAGE ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "WELCOME TO SPARTA BOT")

# --- 4. TEXT & IMAGE PROCESSING ---
@bot.message_handler(content_types=['text', 'photo'])
def handle_all_messages(message):
    try:
        # Loading Animation Icon
        sent_msg = bot.reply_to(message, "🔍 **SPARTA ANALYZE...**", parse_mode='Markdown')
        
        if message.content_type == 'photo':
            # Image download logic
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            # Gemini ko image format batana zaroori hai
            img_data = {
                'mime_type': 'image/jpeg',
                'data': downloaded_file
            }
            
            prompt = message.caption if message.caption else "Analyze this question and provide a step-by-step solution."
            response = model.generate_content([prompt, img_data])
        else:
            # Text query logic
            response = model.generate_content(message.text)

        # Final Formatting
        final_output = f"✨ **SPARTA ANALYZE** ✨\n\n{response.text}"
        
        # 'Analyze...' text ko final answer se edit karna
        bot.edit_message_text(final_output, chat_id=message.chat.id, message_id=sent_msg.message_id, parse_mode='Markdown')

    except Exception as e:
        # Error handling agar API ya network issue ho
        bot.reply_to(message, f"❌ **Error:** {str(e)}")

# --- 5. EXECUTION ---
if __name__ == "__main__":
    keep_alive() # Render port fix start
    print("Sparta Bot is Live!")
    bot.infinity_polling()
