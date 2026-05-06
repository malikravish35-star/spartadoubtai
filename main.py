import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import time

# --- 1. RENDER PORT FIX (FLASK) ---
app = Flask('')

@app.route('/')
def home():
    return "Sparta Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. BOT & AI CONFIGURATION ---
# Render ke Environment Variables se keys uthayega
TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_KEY = os.getenv('GEMINI_KEY')

genai.configure(api_key=GEMINI_KEY)
# gemini-1.5-flash images aur fast response ke liye best hai
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TOKEN)

# --- 3. WELCOME MESSAGE ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "WELCOME TO SPARTA BOT")

# --- 4. MAIN LOGIC (TEXT + IMAGE) ---
@bot.message_handler(content_types=['text', 'photo'])
def handle_all_messages(message):
    try:
        # Loading Animation Icon
        sent_msg = bot.reply_to(message, "🔍 **SPARTA ANALYZE...**", parse_mode='Markdown')
        
        response_text = ""
        
        if message.content_type == 'photo':
            # Image download process
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            with open("temp_image.jpg", "wb") as f:
                f.write(downloaded_file)
            
            # Gemini Vision Processing
            sample_file = genai.upload_file(path="temp_image.jpg", display_name="User_Query")
            
            # Agar image ke saath text bhi bheja hai (caption)
            prompt = message.caption if message.caption else "Analyze this image and provide a detailed solution."
            
            response = model.generate_content([sample_file, prompt])
            response_text = response.text
        else:
            # Only Text Processing
            response = model.generate_content(message.text)
            response_text = response.text

        # Final Formatting
        final_output = f"✨ **SPARTA ANALYZE** ✨\n\n{response_text}"
        
        # Pehle wale 'Analyze...' message ko update karna final answer se
        bot.edit_message_text(final_output, chat_id=message.chat.id, message_id=sent_msg.message_id, parse_mode='Markdown')

    except Exception as e:
        bot.reply_to(message, f"❌ **Error:** {str(e)}")

# --- 5. EXECUTION ---
if __name__ == "__main__":
    keep_alive() # Flask start karega taaki Render port error na de
    print("Sparta Bot is Live and Ready!")
    bot.infinity_polling()
