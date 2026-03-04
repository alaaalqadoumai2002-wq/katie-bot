import os
import random
import threading
import asyncio
import urllib.parse
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- إعداد Flask لضمان استقرار السيرفر على Render ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "Katie is the Absolute Queen! 👑", 200

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# --- التوكن الخاص بكِ ---
TOKEN = "8423220635:AAH4TLlf4MZunC63X-oGMQDPohtyaNKnO28"

# --- بنك البيانات ---
SPECIAL_NAMES = {
    "أحمد": "أومج! أحمد هاد المنور الجروب كله؟ أهلاً يا بطل! ✨",
    "سارة": "سارة؟ هاي الحب والقلب، نورتي يا قمر الجروب 🌸"
}

PRETTY_PICS = ["https://pic.i7lm.com/wp-content/uploads/2019/07/%D8%B5%D9%88%D8%B1-%D8%A8%D9%86%D8%A7%D8%AA-%D9%83%D9%8A%D9%88%D8%AA-%D8%AC%D8%AF%D9%8A%D8%AF%D8%A9.jpg"]
FUNNY_PICS = ["https://pbs.twimg.com/media/E1fH5ZLX0AM3_QY.jpg"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! أنا كاتي 🌸 صاحبة أقوى شخصية في تليجرام.. اكتبي 'قائمة' وشوفي الدلع وقصف الجبهات!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text
    user_text = text.lower()
    user_name = update.effective_user.first_name

    # 1. الرد المخصص للأسماء والترحيب VIP
    for name, response in SPECIAL_NAMES.items():
        if name in text:
            await update.message.reply_text(response)
            return

    if any(word in user_text for word in ["أنا جيت", "باك", "نورت", "جيت"]):
        await update.message.reply_text(f"أطلق باك ونورتي الدنيا يا {user_name}! كاتي كانت مستنيتك 🌸✨")
        return

    # 2. ميزة "زوجني" و "رأيك فيني"
    if "زوجني" in user_text or "زواج" in user_text:
        await update.message.reply_text(f"يا {user_name}، لقيت لك عريس لقطة! بس المهر عليكي والزفة والدي جي عليّ 😂💍")
        return

    if "رايك فيني" in user_text or "رأيك فيني" in user_text:
        opinions = [
            "عسل والله، بس لسانك بدو قص! 👅✂️",
            "أذكى وحدة بالجروب بعدي طبعاً 💅✨",
            "شايفة إنك Red Flag متحرك بس بنحبك 😂🚩",
            "طيوبة وقلبك أبيض مثل الثلج 🌸"
        ]
        await update.message.reply_text(f"رأيي فيكي يا {user_name}: {random.choice(opinions)}")
        return

    # 3. توقعات الفنجان ونسبة الحب
    if "فنجان" in user_text or "توقعي" in user_text:
        predictions = [
            "شايفة في فنجانك خبر حلو رح يوصلك.. بس انتبهي من العين! 🧿✨",
            "في طريقك سفرة قريبة.. غالباً للمطبخ بس معليش 😂☕",
            "شايفة شخص بيفكر فيكي.. بس غالباً بده منك مصاري! 💸🤣"
        ]
        await update.message.reply_text(f"يا {user_name}، كاتي قرأت فنجانك وشافت:\n{random.choice(predictions)}")
        return

    if "نسبة الحب" in user_text:
        score = random.randint(1, 100)
        comment = "حبك برص! انطمي أحسن 😂" if score < 40 else "يا ويلي على الحب والعصافير 😍🔥"
        await update.message.reply_text(f"نسبة الحب لـ {user_name} هي: {score}% ❤️\n{comment}")
        return

    # 4. ردود بحبك وبكرهك (لهجات متعددة)
    if any(word in user_text for word in ["بحبك", "احبك"]):
        replies = ["وأنا كمان بحبني.. ذوقك عالي! 😂❤️", "تؤبريني شو مهضومة.. وأنا بحبك كتير! 🇱🇧✨", "يا لهوي! ده أنا قلبي هيوقف من الكسوف 😍🇪🇬", "أحبش واجد يا بعد روح كاتي! 🇸🇦🔥"]
        await update.message.reply_text(random.choice(replies))
        return

    elif any(word in user_text for word in ["بكرهك", "اكرهك"]):
        replies = ["أحسن! القلوب عند بعضها 😌💅", "منيح اللي قلتي، وفّرتي عليي تفكير! 😂", "انطمي بس.. أنا اللي ميتة فيكي؟ 🙄🇸🇦", "اشربي مية مالح بلكي تتخللي! 🇪🇬🤣"]
        await update.message.reply_text(random.choice(replies))
        return

    # 5. ردود "بوت" (أنا أذكى منك انطم)
    if "بوت" in user_text:
        replies = ["أنا أذكى منك.. انطم! 💅😤", "أنا ذكاء اصطناعي وانتي غباء طبيعي.. انطمي! 🤣", "ناديني كاتي يا عسل بلا بوت بلا هم 🙄"]
        await update.message.reply_text(random.choice(replies))
        return

    # 6. ميزة الشبيه ولقب "مين أنا"
    if any(word in user_text for word in ["شبيهي", "شبيهتي"]):
        choice = random.choice(["pretty", "funny"])
        pic_url = random.choice(PRETTY_PICS if choice == "pretty" else FUNNY_PICS)
        caption = "تفضلي يا قمر 😍" if choice == "pretty" else "لقيت شبيهك انطم لا تعصبي 😂📸"
        try: await update.message.reply_photo(photo=pic_url, caption=caption)
        except: await update.message.reply_text(f"{caption}\n(الرابط: {pic_url})")
        return

    if "مين انا" in user_text or "لقبي" in user_text:
        titles = ["ملكة النكد 👑", "فخر الجروب ✨", "الـ Red Flag المتحرك 🚩😂", "قمر الزمان 🌙", "أطلق واحدة بالكون 💅"]
        await update.message.reply_text(f"لقبك عند كاتي هو: {random.choice(titles)}")
        return

    # 7. الألعاب (لغز / اعتراف) والتشغيل
    if "لغز" in user_text:
        await update.message.reply_text("لغز لعيونك: شيء يطير وليس له جنحان، ويبكي وليس له عينان؟ 🧩\n(الجواب بعد 5 ثواني)")
        await asyncio.sleep(5)
        await update.message.reply_text("الجواب: السحاب ☁️")
        return

    if "اعتراف" in user_text:
        questions = ["شو أكثر شي بتندم عليه؟ 🤐", "مين الشخص اللي لفت انتباهك بالجروب؟ 😉", "شو أكبر كذبة حكيتها؟"]
        await update.message.reply_text(f"سؤال اعتراف لـ {user_name}:\n{random.choice(questions)}")
        return

    if text.startswith("تشغيل"):
        query = text.replace("تشغيل", "").strip()
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        await update.message.reply_text(f"لبيه! هاد طلبك من عيوني: 🎧\n{url}")
        return

    # 8. القائمة الشاملة والمناداة
    if "قائمة" in user_text:
        menu = (
            "أوامر كاتي الفخمة:\n"
            "1️⃣ تشغيل [اسم أغنية] 🎧\n"
            "2️⃣ فنجان / نسبة الحب ❤️\n"
            "3️⃣ رأيك فيني / زوجني 💍\n"
            "4️⃣ شبيهتي / مين انا 🤔\n"
            "5️⃣ لغز / اعتراف / شعر 📜\n"
            "6️⃣ جربي (بحبك، بكرهك، بوت، كاتي)"
        )
        await update.message.reply_text(menu)
        return

    if "كاتي" in user_text:
        await update.message.reply_text(random.choice(["لبيه؟ ✨", "عيونها! 😍", "أطلق من ينادي! 💃", "نعم؟ بدك شي؟ 😤"]))

# 9. الرد على الصور
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(["يا ويلي على هالجمال! 😍", "فخامة! ✨", "فديت هالذوق! 🌸"]))

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
