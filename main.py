from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime
from dotenv import load_dotenv
import json
import os

load_dotenv()

ADMIN_ID = 7325074035
LOG_FILE = "downloads.txt"
BASE_URL = "https://atlasdroid.com/monetag-app/index.html"

# تسجيل المستخدم مرة واحدة فقط
def log_user_once(user_id, name):
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w', encoding="utf-8").close()
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if any(str(user_id) in line for line in lines):
            return False
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {user_id} - {name}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
    return True

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args

    app_id = args[0] if args else "1"  # القيمة الافتراضية "1" إن لم يُحدد شيء

    new_user = log_user_once(user.id, user.first_name)
    if new_user:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"👤 مستخدم جديد:\nID: `{user.id}`\nName: {user.first_name}\nApp ID: {app_id}",
            parse_mode="Markdown"
        )

    message = (
        "📲 *احصل على أقوى تطبيقات IPTV مجانًا!*\n\n"
        "🎁 شاهد إعلانًا قصيرًا ليظهر لك زر التحميل.\n"
        "👇 اضغط الزر أسفله للمتابعة"
    )

    download_link = f"{BASE_URL}?app={app_id}"

    keyboard = [[InlineKeyboardButton("⬇️ تحميل الآن", url=download_link)]]

    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# تشغيل البوت
if __name__ == '__main__':
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("✅ Bot is running...")
    app.run_polling()
