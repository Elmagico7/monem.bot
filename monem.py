import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading

# 🔹 ضع هنا مفاتيحك
GEMINI_API_KEY = "AIzaSyBKr7_XMqA5aI2t2yFaoe3LKlTRS4fnJwc"
TELEGRAM_TOKEN = "7566194765:AAHx-L635Qk-yYoC0gbkZThoeWL1xfTRb9o"

# 🔹 إعداد Gemini
genai.configure(api_key=GEMINI_API_KEY)

# 🔹 إعداد Flask Web Server صغير
app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "Bot is alive!"

# تشغيل السيرفر في الخلفية
threading.Thread(target=lambda: app_flask.run(host="0.0.0.0", port=3000)).start()

# 🔹 بوت التليجرام
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 أهلاً! أنا بوت Gemini — إسألني أي سؤال بالعربية أو الإنجليزية!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ حدث خطأ: {str(e)}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("✅ البوت شغال الآن باستخدام Gemini 2.0 Flash...")
    app.run_polling()

if __name__ == "__main__":
    main()
