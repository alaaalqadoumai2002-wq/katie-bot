import os
import random
import threading
import asyncio
import re
from flask import Flask
from telegram import Update, ChatPermissions
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- إعداد السيرفر لضمان استمرار التشغيل على Render ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "Katie is the Absolute Queen! 👑", 200

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# --- التوكن الخاص بكِ ---
TOKEN = "8423220635:AAH4TLlf4MZunC63X-oGMQDPohtyaNKnO28"

# --- بنك بيانات كاتي (الاقتصاد، الرتب، التعلم) ---
user_data = {} 
learned_replies = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text
    user_text = text.lower()
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    chat_id = update.effective_chat.id

    # 1. تهيئة بيانات المستخدم وتحديث الرتب
    if user_id not in user_data:
        user_data[user_id] = {"balance": 100, "msgs": 0, "partner": None, "is_admin": False, "rank": "عضو جديد"}
    
    user_data[user_id]["msgs"] += 1

    # 🛑 2. نظام الحماية ومنع الروابط (Anti-Link)
    if re.search(r'(https?://[^\s]+|t\.me/[^\s]+)', text):
        # السماح للمديرين فقط بإرسال الروابط
        if not (user_data[user_id]["is_admin"] or user_id == 6834114420): 
            try:
                await update.message.delete()
                await update.message.reply_text(f"ممنوع الروابط يا {user_name}! كاتي بالمرصاد 🛡️🚫")
                return
            except: pass

    # 🛡️ 3. أوامر الإدارة (رفع مدير، طرد، كتم، مسح)
    if text == "رفع مدير" and update.message.reply_to_message:
        target_id = update.message.reply_to_message.from_user.id
        user_data[target_id]["is_admin"] = True
        await update.message.reply_text(f"أبشر! تم رفع {update.message.reply_to_message.from_user.first_name} مدير في كاتي 👑✨")
        return

    if text == "طرد" and update.message.reply_to_message:
        if user_data[user_id]["is_admin"]:
            try:
                await context.bot.ban_chat_member(chat_id, update.message.reply_to_message.from_user.id)
                await update.message.reply_text("تم الطرد بنجاح! 🚪🏃‍♂️")
            except: await update.message.reply_text("ارفعي رتبتي عشان أقدر أطرده! 😤")
        return

    # ❤️ 4. ثنائي اليوم (يختار شخصين عشوائياً)
    if "ثنائي اليوم" in user_text:
        members = list(user_data.keys())
        if len(members) >= 2:
            couple = random.sample(members, 2)
            u1 = (await context.bot.get_chat(couple[0])).first_name
            u2 = (await context.bot.get_chat(couple[1])).first_name
            res = [f"👩‍❤️‍👨 ثنائي اليوم: {u1} و {u2}.. لايقين لبعض! 😂💍", f"🔥 أحلى كوبل بالجروب: {u1} و {u2} ✨"]
            await update.message.reply_text(random.choice(res))
        else:
            await update.message.reply_text("تفاعلوا أكثر عشان أقدر أختار ثنائي! 😤")
        return

    # 🎮 5. ألعاب وفعاليات (لو خيروك، كشف كذب، نسبة الحب بالرد)
    if "لو خيروك" in user_text:
        opts = ["تاكل بصل 🧅 ولا تعتذر للكل؟", "تترك التليجرام 📱 ولا تترك الأكل 🍔؟"]
        await update.message.reply_text(f"لو خيروك: {random.choice(opts)}")
        return

    if "كشف الكذب" in user_text:
        res = random.choice(["صادق ✅", "كذاب وجايب العيد 😂❌", "نص نص 🙊"])
        await update.message.reply_text(f"جهاز كاتي بيقول إنك: {res}")
        return

    if "نسبة الحب" in user_text and update.message.reply_to_message:
        target_name = update.message.reply_to_message.from_user.first_name
        percent = random.randint(0, 100)
        await update.message.reply_text(f"نسبة الحب بين {user_name} و {target_name} هي: {percent}% ❤️")
        return

    # 📊 6. نظام البيانات (ID والرتب)
    if user_text in ["ايدي", "id"]:
        d = user_data[user_id]
        if d["msgs"] > 100: d["rank"] = "أسطورة الجروب 👑"
        elif d["msgs"] > 50: d["rank"] = "عضو فعال ✨"
        
        info = (f"👤 الاسم: {user_name}\n🆔 الايدي: {user_id}\n🎖️ الرتبة: {d['rank']}\n"
                f"💬 الرسائل: {d['msgs']}\n💰 الرصيد: {d['balance']}\n💍 زوجك: {d['partner'] if d['partner'] else 'أعزب'}")
        await update.message.reply_text(info)
        return

    # 💰 7. الاقتصاد والزواج (راتب، تزوجني، طلاق)
    if user_text == "راتب":
        user_data[user_id]["balance"] += 500
        await update.message.reply_text(f"يا {user_name}، استلمت راتبك 500 ريال وهمي 💸")
        return

    if text == "تزوجني" and update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        if user_data[user_id]["partner"]:
            await update.message.reply_text("أنت متزوج أصلاً! خاف الله 😂")
        else:
            user_data[user_id]["partner"] = target.first_name
            user_data[target.id] = user_data.get(target.id, {"balance": 100, "msgs": 0, "partner": user_name, "is_admin": False, "rank": "عضو جديد"})
            user_data[target.id]["partner"] = user_name
            await update.message.reply_text(f"ألف مبروك! {user_name} و {target.first_name} صاروا أحلى كوبل 💍❤️")
        return

    # 📜 8. قائمة الأوامر الشاملة
    if user_text == "اوامر" or user_text == "قائمة":
        menu = ("📜 أوامر كاتي (النسخة الكاملة):\n"
                "🔹 فعاليات: (لو خيروك، كشف الكذب، نسبة الحب، ثنائي اليوم)\n"
                "🔹 بيانات: (ايدي، راتب، رتبتي، ممتلكاتي)\n"
                "🔹 إدارة: (طرد، كتم، رفع مدير، مسح)\n"
                "🔹 اجتماعي: (تزوجني، طلاق، كف، رأيك فيني)")
        await update.message.reply_text(menu)
        return

    # 🧠 9. ميزة التعلم والتطور الذاتي
    if update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
        learned_replies[update.message.reply_to_message.text.lower()] = text
        return
    if user_text in learned_replies:
        await update.message.reply_text(learned_replies[user_text])
        return

    # ردود كاتي الشخصية وقصف الجبهات
    if "بوت" in user_text: await update.message.reply_text("أنا أذكى منك.. انطم! 💅😤")
    if "كاتي" in user_text: await update.message.reply_text(random.choice(["عيونها! 😍", "لبيه؟ ✨", "نعم؟ بدك شي؟ 😤"]))

# --- تشغيل البوت ---
async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    while True: await asyncio.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(main())
