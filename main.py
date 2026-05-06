# Bot Logic (Updated for Hinglish & Concise answers)
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
