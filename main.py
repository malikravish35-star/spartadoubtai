import os
import requests
from flask import Flask, request, jsonify
from openai import OpenAI

# --- 1. CONFIGURATION ---
# Render Dashboard -> Environment Variables mein OPENAI_API_KEY set karein
# Ya fir niche "YOUR_OPENAI_KEY" ki jagah apni key daalein
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_KEY_HERE"))

app = Flask(__name__)

# --- 2. BOT LOGIC ---

@app.route('/')
def home():
    return "Sparta Bot (OpenAI Version) is Running!", 200

@app.route('/webhook', methods=['POST'])
def bot_webhook():
    try:
        data = request.get_json()
        
        # Telegram/n8n se aane wala message handle karna
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            user_text = data["message"].get("text", "")

            if user_text:
                # OpenAI API Call (GPT-3.5 or GPT-4o-mini)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # Aap "gpt-3.5-turbo" bhi use kar sakte hain
                    messages=[{"role": "user", "content": user_text}]
                )
                bot_reply = response.choices[0].message.content
            else:
                bot_reply = "Please send a text message."

            # Note: Yahan aap apni Telegram SendMessage API call add kar sakte hain
            print(f"Chat ID: {chat_id} | Reply: {bot_reply}")

        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# --- 3. RENDER PORT FIX (CRITICAL) ---
if __name__ == "__main__":
    # Render hamesha 'PORT' variable provide karta hai. 
    # Agar wo na mile toh 8080 default rahega.
    port = int(os.environ.get("PORT", 8080))
    
    print("------------------------------------")
    print(f"🚀 Sparta Bot Starting...")
    print(f"📡 Listening on Port: {port}")
    print("------------------------------------")
    
    # host='0.0.0.0' Render ke liye mandatory hai
    app.run(host="0.0.0.0", port=port, debug=False)
