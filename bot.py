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
def health_check(): return "Katie is the Queen of the Group! 👑", 200

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

    # 💰 نظام البنك (مثل طبوش)
    if user_id not in user_data:
        user_data[user_id] = {"balance": 1000, "msgs": 0, "rank": "عضو جديد", "is_admin": False}
    user_data[user_id]["msgs"] += 1

    # 🛑 1. الحماية الفولاذية
    if re.search(r'(https?://[^\s]+|t\.me/[^\s]+)', text):
        if not (user_data[user_id]["is_admin"] or user_id == 6834114420): 
            try: await update.message.delete(); return
            except: pass

    # 👤 2. الاختصارات ( ا / ايدي ) مع التنسيق الفخم وصورة الملف
    if user_text in ["ا", "ايدي", "id"]:
        d = user_data[user_id]
        if d["msgs"] > 500: d["rank"] = "أطلق واحدة بالكون 👑"
        elif d["msgs"] > 100: d["rank"] = "أسطورة الجروب ✨"
        
        info = (
            f"┌─「 معلومات الملكة/الملك 」\n"
            f"├ الاسم : {user_name}\n"
            f"├ الايدي : `{user_id}`\n"
            f"├ الرتبة : {d['rank']}\n"
            f"├ الرسائل : {d['msgs']}\n"
            f"├ الرصيد : {d['balance']} 💰\n"
            f"└─「 كاتي ترحب بكِ 🌸 」"
        )
        try:
            photos = await context.bot.get_user_profile_photos(user_id)
            if photos.total_count > 0:
                await update.message.reply_photo(photo=photos.photos[0][-1].file_id, caption=info, parse_mode='Markdown')
            else: await update.message.reply_text(info, parse_mode='Markdown')
        except: await update.message.reply_text(info, parse_mode='Markdown')
        return

    # 💸 3. نظام الاقتصاد المطور (زرف، بخشيش، راتب)
    if user_text == "راتب":
        gain = random.randint(300, 700)
        user_data[user_id]["balance"] += gain
        await update.message.reply_text(f"💳 تم إيداع {gain} ريال في حسابك البنكي ✨\n💰 رصيدك الحالي: {user_data[user_id]['balance']}")
        return

    if user_text == "زرف" and update.message.reply_to_message:
        target_id = update.message.reply_to_message.from_user.id
        target_name = update.message.reply_to_message.from_user.first_name
        if user_data.get(target_id, {}).get("balance", 0) > 100:
            stolen = random.randint(50, 100)
            user_data[target_id]["balance"] -= stolen
            user_data[user_id]["balance"] += stolen
            await update.message.reply_text(f"😈 كفو! زرفت {stolen} ريال من {target_name} بنجاح ✅")
        else: await update.message.reply_text("طفران ما معه شي تزرفه 😂💸"); return

    if user_text == "بخشيش":
        tip = random.randint(50, 150)
        user_data[user_id]["balance"] += tip
        await update.message.reply_text(f"🎁 كاتي أعطتك بخشيش {tip} ريال.. لا تصرفيهم كلهم! 😉"); return

    # ❤️ 4. ثنائي اليوم (بلمسة طبوش)
    if user_text == "ثنائي اليوم":
        members = list(user_data.keys())
        if len(members) >= 2:
            couple = random.sample(members, 2)
            u1 = (await context.bot.get_chat(couple[0])).first_name
            u2 = (await context.bot.get_chat(couple[1])).first_name
            await update.message.reply_text(f"✨ ثنائي اليوم الأكثر حظاً :\n💍 {u1} ❤️ {u2}\n\nكاتي بتقول: لايقين لبعض! 😍")
        else: await update.message.reply_text("الجروب لسه هادي.. تفاعلوا عشان أختار كوبل! ✨"); return

    # 🎮 5. الألعاب وردود الفعل (بحبك، كاتي، مين انا)
    if any(word in user_text for word in ["بحبك", "احبك"]):
        await update.message.reply_text(random.choice(["وأنا كمان بحبني.. ذوقك عالي! 😂❤️", "يا ويلي على الحب والكسوف 😍✨", "تؤبريني شو مهضومة! 🌸"])); return

    if "مين انا" in user_text:
        await update.message.reply_text(f"أنتِ {random.choice(['قمر الجروب 🌙', 'ملكة النكد 👑', 'أذكى واحدة 💅', 'الـ Red Flag 🚩'])}"); return

    if "كاتي" in user_text:
        await update.message.reply_text(random.choice(["عيونها؟ 😍", "لبيه يا عسل ✨", "نعم؟ في شي؟ 😤"])); return

    # 🧠 6. التعلم السريع (الرد على كاتي)
    if update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
        learned_replies[update.message.reply_to_message.text.lower()] = text
        await update.message.reply_text("✅ كاتي طورت ذكاءها وتعلمت الرد!"); return

    if user_text in learned_replies:
        await update.message.reply_text(learned_replies[user_text]); return

    # 📜 7. القائمة (مزخرفة وفخمة)
    if user_text in ["اوامر", "قائمة"]:
        menu = (
            "╭───「 أوامر كاتي الفخمة 」───\n"
            "│ 💰 البنك: (ا، ايدي، راتب، زرف، بخشيش)\n"
            "│ 🎮 ألعاب: (ثنائي اليوم، لو خيروك، كشف الكذب)\n"
            "│ ❤️ تفاعل: (بحبك، بكرهك، رأيك، مين انا)\n"
            "│ 🛡️ الإدارة: (رفع مدير، طرد، كتم)\n"
            "╰───────────────────"
        )
        await update.message.reply_text(menu); return

async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await application.initialize(); await application.start(); await application.updater.start_polling()
    while True: await asyncio.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(main())
