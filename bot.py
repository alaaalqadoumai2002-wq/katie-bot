import os
import random
import threading
import asyncio
import urllib.parse
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# إعداد Flask عشان Render ما يطفي البوت
app = Flask(__name__)
@app.route('/')
def health_check(): return "Katie is Iconic & Online", 200
def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# التوكن الجديد الصحيح اللي بعتيه هسا
TOKEN = "8423220635:AAH4TLlf4MZunC63X-oGMQDPohtyaNKnO28"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا والله! كاتي وصلت 😂✨\nأنا البوت اللي رح يطير حواجبكم.. اكتبي 'قائمة' وشوفي الدلع والقصف!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_text = text.lower()
    user_name = update.effective_user.first_name

    # --- 1. ميزة تشغيل الأغاني ---
    if text.startswith("تشغيل"):
        query = text.replace("تشغيل", "").strip()
        if query:
            search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            await update.message.reply_text(f"لبيه يا بعد روح كاتي! جاري البحث عن '{query}'... 🎧\nتفضلي الرابط:\n{search_url}")
        else:
            await update.message.reply_text("يا بعد روحها لكاتي، اكتبي اسم الأغنية بعد كلمة تشغيل! 🙄")

    # --- 2. ميزة الرومانسية والهبل ---
    elif any(word in user_text for word in ["بحبك", "احبك"]):
        await update.message.reply_text(random.choice([
            "وأنا كمان بحبني.. ذوقك عالي! 😂❤️",
            "يا عيني! هسا بستحي وبفصل السيرفر 😍",
            "حبك برص.. قصدي حبك بالقلب والله 😂",
            "طيب والمهر؟ اتفقنا على الـ 1000 جيجا؟ 💍🤣"
        ]))

    elif any(word in user_text for word in ["بكرهك", "اكرهك"]):
        await update.message.reply_text(random.choice([
            "أحسن! أصلاً القلوب عند بعضها 😌💅",
            "وفرت عليّ كهرباء وتفكير، شكراً! 😂",
            "ما خصك، حدا طلب رأيك؟ 🙄🤣"
        ]))

    # --- 3. قصف الجبهات (محد طلب رأيك / اخرس) ---
    elif any(word in user_text for word in ["ليش", "كيف", "مين قال", "شو دخلك"]):
        await update.message.reply_text(random.choice([
            "محد طلب رأيك يا قلبي ✨",
            "شو دخلك؟ خليك في حالك أحلنا 💁‍♀️",
            "اخرس شوي خليني أركز 😂",
            "ما خصك، خصوصيات كاتي!"
        ]))

    # --- 4. الألغاز والشعر (يا بعد روحها لكاتي) ---
    elif "لغز" in user_text:
        await update.message.reply_text(f"لبيه يا {user_name}! يا بعد روحها لكاتي، هاد لغز:\nشيء يطير وليس له جنحان، ويبكي وليس له عينان؟")

    elif "شعر" in user_text:
        poems = [
            "يا ليل طوّل شوية.. الحليوة نايم في عينيه ✨",
            "طلتك مثل القمر.. تجلي عن قلبي الكدر 🌸",
            "كاتي يا ست البنات.. كلك ذوق وحركات 💅"
        ]
        await update.message.reply_text(random.choice(poems))

    # --- 5. ردود متنوعة (حظك، كاتي) ---
    elif "حظي اليوم" in user_text:
        await update.message.reply_text("حظك نار! رح تلاقي مصاري ببنطلون قديم 💸✨")

    elif "كاتي" in user_text:
        await update.message.reply_text(random.choice(["عيونها! 😍", "لبيه؟ ✨", "شو بدك؟ 🤣", "أطلق من ينادي!"]))

    elif "قائمة" in user_text:
        await update.message.reply_text("تدللي يا عيوني:\n1️⃣ تشغيل [اسم أغنية] 🎧\n2️⃣ اطلبي 'لغز' 🧩\n3️⃣ اطلبي 'شعر' 📜\n4️⃣ 'حظي اليوم' ✨\n5️⃣ قولي 'بحبك' أو 'بكرهك' وشوفي الرد 😂")

# ميزة الرد على الصور (غزل)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice([
        "يا ويلي على هالجمال! 😍",
        "شو ه الصورة اللي تفتح النفس؟ ✨",
        "فديت هالذوق أنا! 🌸"
    ]))

async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(main())
