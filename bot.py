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
def health_check(): return "Katie is Everything! 👑", 200

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

TOKEN = "8423220635:AAH4TLlf4MZunC63X-oGMQDPohtyaNKnO28"

# --- بنك البيانات ---
user_data = {} 
learned_replies = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text
    user_text = text.lower().strip()
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    chat_id = update.effective_chat.id

    # تهيئة البيانات
    if user_id not in user_data:
        user_data[user_id] = {"balance": 100, "msgs": 0, "partner": None, "is_admin": False, "rank": "عضو جديد"}
    user_data[user_id]["msgs"] += 1

    # 🛑 1. الحماية (منع الروابط)
    if re.search(r'(https?://[^\s]+|t\.me/[^\s]+)', text):
        if not (user_data[user_id]["is_admin"] or user_id == 6834114420): 
            try: await update.message.delete(); return
            except: pass

    # ✨ 2. الردود العاطفية والكوميدية (اللي كانت مفقودة)
    if any(word in user_text for word in ["بحبك", "احبك"]):
        replies = ["وأنا كمان بحبني.. ذوقك عالي! 😂❤️", "تؤبريني شو مهضومة.. وأنا بحبك كتير! ✨", "يا لهوي! ده أنا قلبي هيوقف من الكسوف 😍", "أحبك واجد يا بعد روح كاتي! 🔥"]
        await update.message.reply_text(random.choice(replies)); return

    if any(word in user_text for word in ["بكرهك", "اكرهك"]):
        replies = ["أحسن! القلوب عند بعضها 😌💅", "منيح اللي قلت، وفّرت عليي تفكير! 😂", "انطمي بس.. أنا اللي ميتة فيكي؟ 🙄", "اشربي مية مالح بلكي تتخللي! 🤣"]
        await update.message.reply_text(random.choice(replies)); return

    if "رايك فيني" in user_text or "رأيك فيني" in user_text:
        opinions = ["عسل والله، بس لسانك بدو قص! 👅✂️", "أذكى وحدة بالجروب بعدي طبعاً 💅✨", "شايفة إنك Red Flag متحرك بس بنحبك 😂🚩", "طيوبة وقلبك أبيض مثل الثلج 🌸"]
        await update.message.reply_text(f"رأيي فيكي يا {user_name}: {random.choice(opinions)} ✨"); return

    if "فنجان" in user_text or "توقعي" in user_text:
        predictions = ["شايفة في فنجانك خبر حلو رح يوصلك.. بس انتبهي من العين! 🧿", "في طريقك سفرة قريبة.. غالباً للمطبخ بس معليش 😂☕", "شايفة شخص بيفكر فيكي.. بس غالباً بده منك مصاري! 💸"]
        await update.message.reply_text(f"يا {user_name}، كاتي قرأت فنجانك وشافت:\n{random.choice(predictions)} ✨"); return

    # ✨ 3. مرحبا والتعلم
    if user_text in ["مرحبا", "مراحب", "هلا"]:
        await update.message.reply_text(f"يا مية هلا بـ {user_name}! نورتي الجروب ✨🌸"); return

    if update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
        learned_replies[update.message.reply_to_message.text.lower()] = text
        await update.message.reply_text(f"تم! كاتي طورت حالها وتعلمت الرد ✅🧠"); return

    if user_text in learned_replies:
        await update.message.reply_text(learned_replies[user_text]); return

    # ❤️ 4. ثنائي اليوم والألعاب
    if "ثنائي اليوم" in user_text:
        members = list(user_data.keys())
        if len(members) >= 2:
            couple = random.sample(members, 2)
            u1 = (await context.bot.get_chat(couple[0])).first_name
            u2 = (await context.bot.get_chat(couple[1])).first_name
            await update.message.reply_text(f"👩‍❤️‍👨 ثنائي اليوم: {u1} و {u2}.. لايقين لبعض! 😂💍")
        else: await update.message.reply_text("تفاعلوا أكثر عشان أختار ثنائي! 😤"); return

    if "لو خيروك" in user_text:
        opts = ["تاكل بصل 🧅 ولا تعتذر للكل؟", "تترك التليجرام 📱 ولا تترك الأكل 🍔؟"]
        await update.message.reply_text(f"لو خيروك: {random.choice(opts)} 🤔"); return

    if "كشف الكذب" in user_text:
        res = random.choice(["صادق ✅", "كذاب وجايب العيد 😂❌", "نص نص 🙊"])
        await update.message.reply_text(f"جهاز كاتي بيقول إنك: {res}"); return

    # 📊 5. ايدي وقائمة
    if user_text in ["ايدي", "id"]:
        d = user_data[user_id]
        info = (f"👤 الاسم: {user_name}\n🆔 الايدي: {user_id}\n🎖️ الرتبة: {d['rank']}\n💬 الرسائل: {d['msgs']}\n💰 الرصيد: {d['balance']}")
        await update.message.reply_text(info); return

    if user_text in ["اوامر", "قائمة"]:
        menu = ("📜 أوامر كاتي الشاملة:\n"
                "🎮 ألعاب: (لو خيروك، كشف كذب، عقاب، ثنائي اليوم)\n"
                "❤️ تفاعل: (بحبك، بكرهك، رأيك فيني، فنجان، نسبة الحب)\n"
                "📊 بيانات: (ايدي، رصيدي، رتبتي، راتب)\n"
                "🛡️ إدارة: (طرد، كتم، رفع مدير)\n"
                "✨ ناديني: (مرحبا، كاتي، بوت)")
        await update.message.reply_text(menu); return

    # ردود كاتي الشخصية
    if "بوت" in user_text: await update.message.reply_text("أنا أذكى منك.. انطم! 💅😤")
    elif "كاتي" in user_text: await update.message.reply_text(random.choice(["عيونها! 😍", "لبيه؟ ✨"]))

async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await application.initialize(); await application.start(); await application.updater.start_polling()
    while True: await asyncio.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(main())
