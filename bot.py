import os
import random
import threading
import asyncio
import re
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- سيرفر الاستقرار لـ Render ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "Katie is the Absolute Boss! 👑", 200

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

TOKEN = "8423220635:AAH4TLlf4MZunC63X-oGMQDPohtyaNKnO28"

# --- قاعدة بيانات كاتي الشاملة ---
user_data = {} 
learned_replies = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text
    user_text = text.lower().strip()
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    chat_id = update.effective_chat.id

    # تهيئة البيانات وتحديث النشاط (مثل طبوش)
    if user_id not in user_data:
        user_data[user_id] = {"balance": 100, "msgs": 0, "partner": None, "is_admin": False, "rank": "عضو جديد"}
    
    user_data[user_id]["msgs"] += 1

    # 🛑 1. الحماية الفولاذية (منع الروابط)
    if re.search(r'(https?://[^\s]+|t\.me/[^\s]+)', text):
        if not (user_data[user_id]["is_admin"] or user_id == 6834114420): 
            try:
                await update.message.delete()
                await update.message.reply_text(f"ممنوع الروابط يا {user_name}! كاتي بالمرصاد 🛡️🚫")
                return
            except: pass

    # ✨ 2. الرد على "مرحبا" ونظام التعلم السريع
    if user_text == "مرحبا" or user_text == "مراحب":
        await update.message.reply_text(f"يا مية هلا بـ {user_name}! نورتي الجروب يا ذوق ✨🌸")
        return

    # نظام التعلم بالرد (بدون جاري المعالجة - استجابة فورية)
    if update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
        original_text = update.message.reply_to_message.text.lower()
        learned_replies[original_text] = text
        await update.message.reply_text(f"تم! كاتي طورت حالها وتعلمت الرد ✅🧠")
        return

    if user_text in learned_replies:
        await update.message.reply_text(learned_replies[user_text])
        return

    # ❤️ 3. ميزة "ثنائي اليوم" (الميزة المفقودة سابقاً)
    if "ثنائي اليوم" in user_text:
        members = list(user_data.keys())
        if len(members) >= 2:
            couple = random.sample(members, 2)
            u1 = (await context.bot.get_chat(couple[0])).first_name
            u2 = (await context.bot.get_chat(couple[1])).first_name
            await update.message.reply_text(f"👩‍❤️‍👨 ثنائي اليوم: {u1} و {u2}.. لايقين لبعض! 😂💍")
        else:
            await update.message.reply_text("تفاعلوا أكثر عشان أقدر أختار ثنائي! 😤")
        return

    # 🎮 4. ألعاب طبوش الكاملة (لو خيروك، كشف كذب، عقاب، نسبة حب)
    if "لو خيروك" in user_text:
        opts = ["تاكل صرصور 🪳 ولا تتروش بمية نار 🔥؟", "تنام بالشارع ⛺ ولا تحذف تليجرام 📱؟"]
        await update.message.reply_text(f"لو خيروك: {random.choice(opts)}")
        return

    if "كشف الكذب" in user_text:
        res = random.choice(["صادق ✅", "كذاب وجايب العيد 😂❌", "نص نص 🙊"])
        await update.message.reply_text(f"جهاز كاتي بيقول إنك: {res}")
        return

    if "عقاب" in user_text:
        punish = random.choice(["تغير اسمك لـ 'أنا بطة' 🦆", "ترسل بصمة غناء 🎤", "تحول 500 للي يرد أولاً 💸"])
        await update.message.reply_text(f"عقابك: {punish}")
        return

    if "نسبة الحب" in user_text and update.message.reply_to_message:
        target_name = update.message.reply_to_message.from_user.first_name
        percent = random.randint(0, 100)
        await update.message.reply_text(f"نسبة الحب بين {user_name} و {target_name} هي: {percent}% ❤️")
        return

    # 📊 5. ايدي (ID) والبيانات والرتب
    if user_text in ["ايدي", "id"]:
        d = user_data[user_id]
        if d["msgs"] > 100: d["rank"] = "أسطورة الجروب 👑"
        elif d["msgs"] > 50: d["rank"] = "عضو فعال ✨"
        info = (f"👤 الاسم: {user_name}\n🆔 الايدي: {user_id}\n🎖️ الرتبة: {d['rank']}\n💬 الرسائل: {d['msgs']}\n💰 الرصيد: {d['balance']}")
        await update.message.reply_text(info)
        return

    # 🛡️ 6. أوامر الإدارة
    if text == "رفع مدير" and update.message.reply_to_message:
        target_id = update.message.reply_to_message.from_user.id
        user_data[target_id]["is_admin"] = True
        await update.message.reply_text(f"تم رفع {update.message.reply_to_message.from_user.first_name} مدير في كاتي 👑")
        return

    # 💰 7. الاقتصاد (راتب)
    if user_text == "راتب":
        user_data[user_id]["balance"] += 500
        await update.message.reply_text(f"استلمت 500 ريال وهمي من كاتي 💸")
        return

    # 📜 8. القائمة الشاملة (للتأكد من وجود كل شيء)
    if user_text in ["اوامر", "قائمة", "الاوامر"]:
        menu = (
            "📜 أوامر كاتي (النسخة النهائية):\n"
            "🎮 ألعاب: (لو خيروك، كشف الكذب، عقاب، ثنائي اليوم)\n"
            "❤️ تفاعل: (نسبة الحب، تزوجني، طلاق، كف)\n"
            "📊 بيانات: (ايدي، رصيدي، رتبتي، راتب)\n"
            "🛡️ إدارة: (طرد، كتم، رفع مدير، مسح)\n"
            "✨ ناديني: (مرحبا، كاتي، بوت)"
        )
        await update.message.reply_text(menu)
        return

    # ردود كاتي الشخصية
    if "بوت" in user_text: await update.message.reply_text("أنا أذكى منك.. انطم! 💅😤")
    if "كاتي" in user_text: await update.message.reply_text(random.choice(["عيونها! 😍", "لبيه؟ ✨"]))

async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await application.initialize(); await application.start(); await application.updater.start_polling()
    while True: await asyncio.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(main())
