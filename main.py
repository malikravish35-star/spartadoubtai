import os
import requests
import google.generativeai as genai
from flask import Flask, request, jsonify

# --- API & MODEL CONFIGURATION ---
# Render dashboard me GEMINI_API_KEY set karein
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_KEY_HERE")
genai.configure(api_key=API_KEY)

# Model setup (v1beta ya 404 error se bachne ke liye standard name)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

# --- CORE BOT LOGIC ---

@app.route('/')
def health_check():
    return "Sparta Bot Status: Online & Running", 200

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    try:
        data = request.get_json()
        
        # Check if message exists in the data
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            user_text = data["message"].get("text", "")

            # Gemini se response generate karna
            if user_text:
                gemini_resp = model.generate_content(user_text)
                final_text = gemini_resp.text
            else:
                final_text = "Mujhe sirf text messages samajh aate hain."

            # Yahan aap apna n8n ya Telegram API ka reply logic daal sakte hain
            # Example: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", ...)
            
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

# --- THE FIX FOR RENDER PORT BINDING ---
# Ye wala part sabse important hai jo aapke logs me error de raha tha
if __name__ == "__main__":
    # Render environment variable se port uthata hai
    # Hardcoded 8080 ya 5000 se deployment fail ho sakti hai
    port = int(os.environ.get("PORT", 8080))
    
    print("------------------------------")
    print(f"🚀 Starting Sparta Bot...")
    print(f"📡 Listening on Port: {port}")
    print("------------------------------")
    
    # 0.0.0.0 host zaroori hai Render ke liye
    app.run(host="0.0.0.0", port=port, debug=False)
