from flask import Flask
from threading import Thread
import telebot
import os
# ... (baaki imports jaise google.generativeai)

# FLASK SERVER (For Render Port)
app = Flask('')
@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# BOT SETUP
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# 1. WELCOME MESSAGE
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "WELCOME SPARTA BOT")

# 2. ANSWER LOGIC
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Yahan aapka Gemini wala code aayega jo answer generate karta hai
    # Maan lijiye answer 'ai_response' mein hai:
    
    ai_response = "Aapka Gemini ka answer yahan aayega..." # Is line ko apne purane Gemini code se replace karein
    
    final_text = f"**SPARTA ANALYZE**\n\n{ai_response}"
    bot.reply_to(message, final_text, parse_mode='Markdown')

if __name__ == "__main__":
    keep_alive()
    print("Bot is starting...")
    bot.infinity_polling()# Bot Logic (Updated for Hinglish & Concise answers)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # Yahan humne instruction badal di hai
        prompt = (
            f"You are a helpful teacher. Solve this doubt in Hinglish (mix of Hindi and English). "
            f"Keep the explanation very concise, easy to understand, and point-to-point. "
            f"Doubt: {user_text}"
        )
        
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Kuch error aaya, please thodi der baad try karein.")
