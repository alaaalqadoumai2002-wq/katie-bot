import os
import random
import asyncio
import threading
import urllib.parse
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- إعداد Flask ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "Katie is Iconic & Online 🌸", 200

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- التوكن الخاص بكِ ---
TOKEN = "8423220635:AAH4TLlf4MZunC63X-oGMQDPohtyaNKnO28"

# --- معالج الرسائل الرئيسي ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_name = update.effective_user.first_name # اسم الشخص اللي بيحكي
    
    # 🌟 1. ميزة الرد المخصص (تقدري تضيفي أسماء قد ما بدك)
    if user_name == "هنا ضعي اسم الشخص": # مثلاً "أحمد"
        await update.message.reply_text("يا مية هلا بأغلى الناس.. نورت كاتي بوجودك! ✨")
        return

    if user_name == "اسم صديقتك": # مثلاً "سارة"
        await update.message.reply_text("سوسو حبيبة قلبي وصلت! شو هالنور؟ 😍🌸")
        return

    # 2. ميزة الشبيه
    if text == "شبيهي":
        img = "https://tse1.mm.bing.net/th?id=OIP.G6v9_H0D_5w7_m7N8W8W7AHaHa&pid=Api"
        await update.message.reply_photo(photo=img, caption=f"شبيهك يا {user_name}.. نسخة منك! 😂")
    elif text == "شبيهتي":
        img = "https://tse4.mm.bing.net/th?id=OIP.J8v9mI8N_v9mI8N_v8W7AHaHa&pid=Api"
        await update.message.reply_photo(photo=img, caption=f"هاي شبيهتك.. قمر بس ناقصك مكياج! 🤣💅")

    # 3. الزواج ونسبة الحب
    elif text in ["تزويج", "زوجيني"]:
        await update.message.reply_text(f"أعلنت زواجك يا {user_name} من شخص سري بالجروب! 💍 مبروك!")
    elif "نسبة حبي" in text:
        await update.message.reply_text(f"نسبة حبك هي {random.randint(1, 100)}%.. كاتي بتقلك كملي! ❤️")

    # 4. ردود الدلع والتعصيب
    elif "بحبك" in text:
        await update.message.reply_text("تؤبشيني! وأنا ميتة فيكي 🌸")
    elif "بكرهك" in text:
        await update.message.reply_text("الغيرة بتعمل أكتر من هيك يا قلبي 💅")
    elif "بوت" in text:
        await update.message.reply_text("بوت في عينك! أنا كاتي ست البنات.. احترمي نفسك! 😡")

    # 5. تشغيل الأغاني
    elif text.startswith("تشغيل"):
        query = text.replace("تشغيل", "").strip()
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        await update.message.reply_text(f"جاري البحث لعيونك... 🎧\nتفضلي:\n{search_url}")

    # 6. القائمة
    elif text == "قائمة":
        await update.message.reply_text("👑 أوامر كاتي:\n🎵 تشغيل\n📸 شبيهي/تي\n💍 تزويج\n❤️ نسبة حبي\n💬 من هي كاتي؟")

# رد كاتي على الصور
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("يا ويلي على هالجمال! 😍 الصورة محلية الجروب")

# --- تشغيل البوت ---
async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    while True: await asyncio.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(main())
