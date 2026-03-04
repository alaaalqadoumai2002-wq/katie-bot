import os
import random
import asyncio
import threading
import urllib.parse
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

# --- إعداد Flask للبقاء حياً على Render ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "Katie is the Queen! 👑", 200

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

# --- التوكن الخاص بكِ ---
TOKEN = "8423220635:AAH4TLlf4MZunC63X-oGMQDPohtyaNKnO28"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! أنا كاتي 🌸 صاحبة أقوى شخصية.. جربي اكتبي 'قائمة' وشوفي الدلع وقصف الجبهات!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text.strip()
    user_text = text.lower()
    user_name = update.effective_user.first_name

    # 1. نظام تشغيل الأغاني (رابط ذكي ومحدد)
    if text.startswith("تشغيل"):
        query = text.replace("تشغيل", "").strip()
        if not query:
            await update.message.reply_text("يا بعد روحها لكاتي، اكتبي اسم الأغنية بعد كلمة تشغيل! 🎧")
            return
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        await update.message.reply_text(f"لبيه! طلبتي {query}؟ هاد طلبك من عيوني يا بعد روحي: 🎧\n{url}")
        return

    # 2. نظام قصف الجبهات (محد طلب رأيك / اخرس)
    # يرد فقط إذا كان الكلام فيه سؤال فضولي أو تدخل
    if any(word in user_text for word in ["ليش", "كيف", "مين قال", "شو دخلك", "ما خصك", "من وين"]):
        replies = [
            "محد طلب رأيك يا قلبي ✨", 
            "شو دخلك؟ خليك في حالك أحلنا 💁‍♀️", 
            "اخرس شوي خليني أركز 😂",
            "ما خصك، خصوصيات بنات!"
        ]
        await update.message.reply_text(random.choice(replies))
        return

    # 3. الألغاز والشعر (بالدلع اللي اتفقنا عليه)
    if "لغز" in user_text:
        await update.message.reply_text(f"لبيه يا {user_name}! يا بعد روحها لكاتي، هاد لغز لعيونك:\nشيء يطير وليس له جنحان، ويبكي وليس له عينان؟")
        return

    if "شعر" in user_text:
        poems = [
            "يا ليل طوّل شوية.. الحليوة نايم في عينيه ✨",
            "طلتك مثل القمر.. تجلي عن قلبي الكدر 🌸",
            "كاتي يا ست البنات.. كلك ذوق وحركات 💅"
        ]
        await update.message.reply_text(random.choice(poems))
        return

    # 4. ردود الحب والرومانسية
    if any(word in user_text for word in ["بحبك", "احبك"]):
        love_replies = [
            "وأنا كمان بحبني.. ذوقك عالي! 😂❤️",
            "يا عيني! هسا بستحي 😍",
            "حبك بالقلب والله يا بعد روح كاتي 😂💍"
        ]
        await update.message.reply_text(random.choice(love_replies))
        return

    # 5. القائمة المنظمة
    if "قائمة" in user_text or "أوامر" in user_text:
        menu_text = (
            "تدللي يا عيوني، كاتي بخدمتك:\n"
            "1️⃣ تشغيل [اسم أغنية] 🎧\n"
            "2️⃣ اطلبي 'لغز' 🧩\n"
            "3️⃣ اطلبي 'شعر' 📜\n"
            "4️⃣ قولي 'حظي اليوم' ✨\n"
            "5️⃣ جربي قولي 'بحبك' أو تدخل بشغلي وشوفي الرد 😂"
        )
        await update.message.reply_text(menu_text)
        return

    # 6. حظك اليوم
    if "حظ" in user_text:
        await update.message.reply_text("حظك نار! رح تلاقي مصاري ببنطلون قديم 💸✨")
        return

    # 7. الرد على اسم "كاتي"
    if "كاتي" in user_text:
        await update.message.reply_text(random.choice(["عيونها! 😍", "لبيه؟ ✨", "أطلق من ينادي! 💃"]))
        return

# 8. الرد على الصور (الغزل)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_replies = [
        "يا ويلي على هالجمال! 😍",
        "شو ه الصورة اللي تفتح النفس؟ ✨",
        "فديت هالذوق أنا! 🌸"
    ]
    await update.message.reply_text(random.choice(photo_replies))

async def main():
    application = Application.builder().token(TOKEN).build()
    
    # إضافة الأوامر والرسائل
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    # البقاء في وضع التشغيل
    while True: await asyncio.sleep(1)

if __name__ == "__main__":
    # تشغيل Flask في خيط منفصل
    threading.Thread(target=run_flask, daemon=True).start()
    # تشغيل البوت
    asyncio.run(main())
