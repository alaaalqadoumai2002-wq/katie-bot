import os
import random
import threading
import asyncio
import urllib.parse
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)
@app.route('/')
def health_check(): return "Katie is the Queen of Everything! 👑", 200
def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

TOKEN = "8423220635:AAH4TLlf4MZunC63X-oGMQDPohtyaNKnO28"

# --- بنك البيانات الشامل ---
SPECIAL_NAMES = {
    "أحمد": "أومج! أحمد هاد المنور الجروب كله؟ أهلاً يا بطل! ✨",
    "سارة": "سارة؟ هاي الحب والقلب، نورتي يا قمر الجروب 🌸"
}

PRETTY_PICS = ["https://i.pinimg.com/736x/0c/3b/6a/0c3b6a9e3b1f3d8a5f5f5f5f5f5f5f5f.jpg"]
FUNNY_PICS = ["https://i.ytimg.com/vi/317n0A8m-H8/maxresdefault.jpg"]

POEMS = ["طلتك مثل القمر.. تجلي عن قلبي الكدر 🌸", "يا ليل طوّل شوية.. الحليوة نايم في عينيه ✨", "كاتي يا ست البنات.. كلك ذوق وحركات 💅"]

CONFESSION_QUESTIONS = ["شو أكثر شي بتندم عليه؟ 🤐", "مين الشخص اللي لفت انتباهك بالجروب؟ 😉", "شو أكبر كذبة حكيتيها؟"]

RIDDLES = [{"q": "شيء يطير وليس له جنحان، ويبكي وليس له عينان؟", "a": "السحاب ☁️"}]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا والله! أنا كاتي 🌸\nصاحبة أقوى شخصية وأذكى ردود.. اكتبي 'قائمة' وشوفي الدلع!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text
    user_text = text.lower()
    user_name = update.effective_user.first_name

    # 1. الرد المخصص للأسماء والترحيب
    for name, response in SPECIAL_NAMES.items():
        if name in text:
            await update.message.reply_text(response)
            return

    if any(word in user_text for word in ["أنا جيت", "باك", "نورت"]):
        await update.message.reply_text(f"أطلق باك! نورتي الدنيا يا {user_name} 🌸✨ كاتي كانت بانتظارك!")
        return

    # 2. ميزة تشغيل الأغاني
    if text.startswith("تشغيل"):
        query = text.replace("تشغيل", "").strip()
        if query:
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            await update.message.reply_text(f"لبيه! جاري البحث عن {query}... 🎧\n{url}")
        return

    # 3. ميزة نسبة الحب وتوقعات الفنجان
    if "نسبة الحب" in user_text:
        score = random.randint(1, 100)
        comment = "حبك برص! قصدي حبكم بالقلب 😂" if score < 40 else "يا ويلي على العشاق 😍🔥"
        await update.message.reply_text(f"نسبة الحب لـ {user_name} هي: {score}% ❤️\n{comment}")
        return

    if "فنجان" in user_text or "توقعي" in user_text:
        predictions = [
            "شايفة في فنجانك خبر حلو رح يوصلك.. بس انتبهي من العين! 🧿✨",
            "في طريقك سفرة قريبة.. غالباً للمطبخ بس معليش 😂☕",
            "شايفة شخص بيفكر فيكي.. بس غالباً بدو منك مصاري! 💸🤣"
        ]
        await update.message.reply_text(f"يا {user_name}، كاتي قرأت فنجانك وشافت:\n{random.choice(predictions)}")
        return

    # 4. ميزة "مين أنا" (لقب مضحك)
    if "مين انا" in user_text or "لقبي" in user_text:
        titles = ["ملكة النكد 👑", "فخر الجروب ✨", "الـ Red Flag المتحرك 🚩😂", "قمر الزمان 🌙", "أطلق واحدة بالكون 💅"]
        await update.message.reply_text(f"لقبك عند كاتي هو: {random.choice(titles)}")
        return

    # 5. الألعاب (لغز، اعتراف، لو خيروك)
    if "لغز" in user_text:
        r = random.choice(RIDDLES)
        await update.message.reply_text(f"لغز لعيونك:\n{r['q']}")
        await asyncio.sleep(5)
        await update.message.reply_text(f"الجواب: {r['a']} 😉")
        return

    if "اعتراف" in user_text:
        await update.message.reply_text(f"سؤال اعتراف لـ {user_name}:\n{random.choice(CONFESSION_QUESTIONS)}")
        return

    # 6. الردود القوية (انطم / أذكى منك)
    if "بوت" in user_text:
        await update.message.reply_text("أنا أذكى منك.. انطم! 💅😤")
        return

    if any(word in user_text for word in ["ليش", "كيف", "شو دخلك"]):
        await update.message.reply_text("محد طلب رأيك، انطم وخليك في حالك! 💁‍♀️✨")
        return

    # 7. ميزة الشبيه
    if any(word in user_text for word in ["شبيهي", "شبيهتي"]):
        choice = random.choice(["pretty", "funny"])
        pic = random.choice(PRETTY_PICS if choice == "pretty" else FUNNY_PICS)
        caption = "تفضلي يا قمر 😍" if choice == "pretty" else "لقيت شبيهك انطم لا تعصبي 😂"
        await update.message.reply_photo(photo=pic, caption=caption)
        return

    # 8. القائمة الشاملة
    if "قائمة" in user_text:
        menu = (
            "أوامر كاتي الفخمة:\n"
            "1️⃣ تشغيل [اسم أغنية] 🎧\n"
            "2️⃣ توقعي / فنجان ☕\n"
            "3️⃣ نسبة الحب ❤️\n"
            "4️⃣ لغز / اعتراف / شعر 📜\n"
            "5️⃣ شبيهتي 📸\n"
            "6️⃣ مين انا (لقبي) 🤔"
        )
        await update.message.reply_text(menu)
        return

    if "كاتي" in user_text:
        await update.message.reply_text(random.choice(["لبيه؟ ✨", "عيونها! 😍", "أطلق من ينادي! 💃"]))

# 9. بصمة كاتي (الرد على الصور والإيموجي)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(["يا ويلي على هالجمال! 😍", "فديت هالذوق الفخم ✨"]))

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
    asyncio.run(main())
