import os
import random
import asyncio
import threading
import urllib.parse
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- إعداد Flask لـ Render ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "Katie is Iconic & Vining! 🌸", 200

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- التوكن الخاص بكِ ---
TOKEN = "8423220635:AAH4TLlf4MZunC63X-oGMQDPohtyaNKnO28"

# --- داتا الردود والقصف والأشعار ---
ROASTS = [
    "وجهك ولا وجه علبة سردين مطعوجة؟ 😂",
    "ثقتك بنفسك بتذكرني بثقة اللابتوب لما يكون شحنه 1% وبيحكي سأعمل! 💻🤣",
    "محد طلب رأيك يا قلبي ✨",
    "شو دخلك؟ خليك في حالك أحلنا 💁‍♀️",
    "ما خصك، خصوصيات بنات! 💅",
    "اخرس شوي خليني أركز 😂",
    "أنا ذكاء اصطناعي وانتي غباء طبيعي.. سبحان الله كيف بنكمل بعض! 🤣"
]

POEMS = [
    "يا ليل طوّل شوية.. \n الحليوة نايم في عينيه ✨",
    "طلتك مثل القمر.. \n تجلي عن قلبي الكدر 🌸",
    "كاتي يا ست البنات.. \n كلك ذوق وحركات 💅"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! أنا كاتي 🌸\nصاحبة أقوى شخصية بالتليجرام.. اكتبي 'قائمة' وشوفي الدلع!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_name = update.effective_user.first_name

    # 1. ميزة تشغيل الأغاني
    if text.startswith("تشغيل"):
        query = text.replace("تشغيل", "").strip()
        if query:
            search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            await update.message.reply_text(f"لعيونك جاري البحث عن '{query}'... 🎧\nتفضلي الرابط:\n{search_url}")
        else:
            await update.message.reply_text("يا بعد روح كاتي، اكتبي اسم الأغنية!")

    # 2. قصف الجبهات وردود "ما خصك"
    elif any(word in text for word in ["ليش", "كيف", "مين قال", "قصف", "اقصفي"]):
        await update.message.reply_text(f"اسمعي يا {user_name}.. {random.choice(ROASTS)}")

    # 3. الألغاز
    elif "لغز" in text:
        await update.message.reply_text(f"لبيه يا {user_name}! يا بعد روحها لكاتي، هاد لغز لعيونك:\nشيء يطير وليس له جنحان، ويبكي وليس له عينان؟ 🧩")

    # 4. الأشعار
    elif "شعر" in text:
        await update.message.reply_text(random.choice(POEMS))

    # 5. ردود الترند
    elif "شو بتعملي" in text:
        await update.message.reply_text("بضبط كحلتي، في شي؟ 💄💅")
    
    # 6. القائمة الكاملة
    elif "قائمة" in text or "اوامر" in text:
        await update.message.reply_text(
            "تدللي يا عيوني أوامر كاتي:\n"
            "1️⃣ تشغيل [اسم الأغنية] 🎵\n"
            "2️⃣ اطلبي 'لغز' 🧩\n"
            "3️⃣ اطلبي 'شعر' 📜\n"
            "4️⃣ اكتبي 'قصف' 💥\n"
            "5️⃣ أرسلي 'صورة' وشوفي ردي! 😍"
        )

# 7. ميزة الرد على الصور
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    res = ["يا ويلي على هالجمال! 😍", "شو ه الصورة اللي تفتح النفس؟ ✨", "فديت هالذوق أنا! 🌸"]
    await update.message.reply_text(random.choice(res))

async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    while True: await asyncio.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
