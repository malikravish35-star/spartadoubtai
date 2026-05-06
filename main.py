import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- 1. RENDER WEB SERVER (PORT FIX) ---
app = Flask('')

@app.route('/')
def home():
    return "Sparta Bot is Online!"

def run():
    # Render hamesha port 8080 ya 10000 ki demand karta hai
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. BOT & GEMINI AI SETUP ---
TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_KEY')

# Transport='rest' lagane se 404/v1beta wala error solve ho jata hai
genai.configure(api_key=GEMINI_KEY, transport='rest')

# Stable model call
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TOKEN)

# --- 3. COMMANDS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "WELCOME TO SPARTA BOT")

# --- 4. MAIN LOGIC (TEXT + PHOTO) ---
@bot.message_handler(content_types=['text', 'photo'])
def handle_message(message):
    try:
        # Initial Analyzing Message
        sent_msg = bot.reply_to(message, "🔍 **SPARTA ANALYZE...**", parse_mode='Markdown')
        
        if message.content_type == 'photo':
            # Image download
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            # Image processing for Gemini
            img_parts = [{"mime_type": "image/jpeg", "data": downloaded_file}]
            prompt = message.caption if message.caption else "Solve this question step by step."
            
            # Response generation
            response = model.generate_content([prompt, img_parts[0]])
        else:
            # Text processing
            response = model.generate_content(message.text)

        # Final Formatting
        final_answer = f"✨ **SPARTA ANALYZE** ✨\n\n{response.text}"
        
        # Answer ko edit karke bhejna
        bot.edit_message_text(final_answer, chat_id=message.chat.id, message_id=sent_msg.message_id, parse_mode='Markdown')

    except Exception as e:
        # Error handling
        bot.edit_message_text(f"❌ **Error:** {str(e)}", chat_id=message.chat.id, message_id=sent_msg.message_id)

# --- 5. RUN BOT ---
if __name__ == "__main__":
    keep_alive() # Background server start
    print("Sparta Bot is Starting...")
    bot.infinity_polling()
