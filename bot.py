import os
import random
from flask import Flask
import threading
import asyncio
import urllib.parse
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# إعداد Flask لإبقاء البوت حياً على Render
app = Flask(__name__)
@app.route('/')
def health_check(): 
    return "Katie is Iconic 🌸 البوت يعمل بنجاح", 200

def run_flask():
    # Render يطلب تشغيل السيرفر على هذا المنفذ
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# التوكن الجديد الخاص بكِ
TOKEN = "8423220635:AAH4TLlf4MZunC63X-oGMQDPohtyaNKnO28"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! أنا كاتي 🌸\nصاحبة أقوى شخصية بالتليجرام.. اكتبي 'قائمة' وشوفي الدلع!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_name = update.effective_user.first_name

    if text.startswith("تشغيل"):
        query = text.replace("تشغيل", "").strip()
        if query:
            search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            await update.message.reply_text(f"لعيونك جاري البحث عن '{query}'... 🎧\nتفضلي النتائج هنا:\n{search_url}")
        else:
            await update.message.reply_text("يا بعد روح كاتي، اكتبي اسم الأغنية!")

    elif any(word in text for word in ["ليش", "كيف", "مين قال"]):
        await update.message.reply_text(random.choice(["محد طلب رأيك يا قلبي ✨", "شو دخلك؟ خليك في حالك أحسن 💁‍♀️", "ما خصك، خصوصيات بنات!"]))

    elif "لغز" in text:
        await update.message.reply_text(f"لبيه يا {user_name}! هاد لغز لعيونك:\nشيء يطير وليس له جنحان، ويبكي وليس له عينان؟")

    elif "شعر" in text:
        poems = ["طلتك مثل القمر.. \n تجلي عن قلبي الكدر 🌸", "كاتي يا ست البنات.. \n كلك ذوق وحركات 💅"]
        await update.message.reply_text(random.choice(poems))
    
    elif "قائمة" in text:
        await update.message.reply_text("تدللي يا عيوني:\n1️⃣ تشغيل [اسم الأغنية]\n2️⃣ لغز 🧩\n3️⃣ شعر 📜\n4️⃣ أرسلي صورة!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("يا ويلي على هالجمال! 😍✨")

async def main():
    # بناء التطبيق
    application = Application.builder().token(TOKEN).build()
    
    # إضافة الأوامر والمستقبلات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # بدء البوت
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    # إبقاء البوت قيد التشغيل
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    # تشغيل Flask في الخلفية لإرضاء Render
    threading.Thread(target=run_flask, daemon=True).start()
    
    # تشغيل محرك البوت الأساسي
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
