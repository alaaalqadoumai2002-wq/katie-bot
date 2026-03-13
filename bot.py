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
def health_check(): return "Katie Bank & Games Online! 👑", 200

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

TOKEN = "8423220635:AAH4TLlf4MZunC63X-oGMQDPohtyaNKnO28"

# --- قاعدة البيانات ---
user_data = {} 
learned_replies = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text
    user_text = text.lower().strip()
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    chat_id = update.effective_chat.id

    # 💰 تهيئة الحساب البنكي (فتح حساب تلقائي)
    if user_id not in user_data:
        user_data[user_id] = {
            "balance": 1000, # رصيد افتتاحي
            "msgs": 0, 
            "rank": "عضو جديد",
            "is_admin": False
        }
    user_data[user_id]["msgs"] += 1

    # 🛑 1. الحماية
    if re.search(r'(https?://[^\s]+|t\.me/[^\s]+)', text):
        if not (user_data[user_id]["is_admin"] or user_id == 6834114420): 
            try: await update.message.delete(); return
            except: pass

    # 👤 2. ايدي (أو اختصار "ا") مع صورة الملف الشخصي
    if user_text in ["ايدي", "id", "ا"]:
        d = user_data[user_id]
        photos = await context.bot.get_user_profile_photos(user_id)
        info = (f"👤 الاسم: {user_name}\n🆔 الايدي: {user_id}\n🎖️ الرتبة: {d['rank']}\n"
                f"💬 الرسائل: {d['msgs']}\n💰 رصيدك البنكي: {d['balance']} ريال 💸")
        
        if photos.total_count > 0:
            await update.message.reply_photo(photo=photos.photos[0][-1].file_id, caption=info)
        else:
            await update.message.reply_text(info)
        return

    # 💸 3. نظام الاقتصاد (راتب، استثمار، زرف، بخشيش)
    if user_text == "راتب":
        gain = random.randint(200, 500)
        user_data[user_id]["balance"] += gain
        await update.message.reply_text(f"💰 تم إضافة {gain} ريال لحسابك البنكي يا {user_name}! رصيدك الآن: {user_data[user_id]['balance']}")
        return

    if user_text == "بخشيش":
        tip = random.randint(10, 100)
        user_data[user_id]["balance"] += tip
        await update.message.reply_text(f"🎁 كاتي أعطتك بخشيش {tip} ريال يا كريم!")
        return

    if user_text == "استثمار":
        if user_data[user_id]["balance"] < 100:
            await update.message.reply_text("لازم يكون معك 100 ريال على الأقل للاستثمار! ❌")
        else:
            outcome = random.choice(["win", "lose"])
            amount = random.randint(50, 200)
            if outcome == "win":
                user_data[user_id]["balance"] += amount
                await update.message.reply_text(f"📈 استثمار ناجح! ربحت {amount} ريال. رصيدك: {user_data[user_id]['balance']}")
            else:
                user_data[user_id]["balance"] -= amount
                await update.message.reply_text(f"📉 للأسف خسر الاستثمار {amount} ريال. رصيدك: {user_data[user_id]['balance']}")
        return

    if user_text == "زرف" and update.message.reply_to_message:
        target_id = update.message.reply_to_message.from_user.id
        target_name = update.message.reply_to_message.from_user.first_name
        if user_data.get(target_id, {}).get("balance", 0) > 50:
            stolen = random.randint(10, 50)
            user_data[target_id]["balance"] -= stolen
            user_data[user_id]["balance"] += stolen
            await update.message.reply_text(f"😈 زرفت {stolen} ريال من {target_name} بنجاح!")
        else:
            await update.message.reply_text(f"يا حرام {target_name} طفران، ما عنده شي تزرفه! 😂")
        return

    # ❤️ 4. ثنائي اليوم والألعاب
    if "ثنائي اليوم" in user_text:
        members = list(user_data.keys())
        if len(members) >= 2:
            couple = random.sample(members, 2)
            u1 = (await context.bot.get_chat(couple[0])).first_name
            u2 = (await context.bot.get_chat(couple[1])).first_name
            await update.message.reply_text(f"👩‍❤️‍👨 ثنائي اليوم: {u1} و {u2}.. مبروك مقدماً! 💍")
        return

    # ✨ 5. مرحبا والتعلم
    if user_text in ["مرحبا", "مراحب", "هلا"]:
        await update.message.reply_text(f"يا مية هلا بـ {user_name}! نورتي الجروب ✨🌸"); return

    if update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
        learned_replies[update.message.reply_to_message.text.lower()] = text
        await update.message.reply_text(f"تم! كاتي طورت حالها وتعلمت الرد ✅🧠"); return

    if user_text in learned_replies:
        await update.message.reply_text(learned_replies[user_text]); return

    # 📜 6. القائمة
    if user_text in ["اوامر", "قائمة"]:
        menu = (
            "📜 أوامر كاتي البنكية:\n"
            "💰 اقتصاد: (ا، ايدي، راتب، استثمار، زرف، بخشيش)\n"
            "🎮 ألعاب: (ثنائي اليوم، لو خيروك، كشف الكذب)\n"
            "❤️ تفاعل: (بحبك، بكرهك، رأيك فيني)\n"
            "🛡️ إدارة: (رفع مدير، طرد)"
        )
        await update.message.reply_text(menu); return

    # ردود كاتي
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
