import os
import random
import asyncio
import threading
import urllib.parse
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- إعداد Flask لـ Render ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "Katie is Diva! 💅", 200

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- التوكن (تأكدي أنه صحيح) ---
TOKEN = "8423220635:AAH4TLlf4MZunC63X-oGMQDPohtyaNKnO28"

# --- داتا الألعاب والصور ---
ROASTS = [
    "وجهك ولا وجه علبة سردين مطعوجة؟ 😂",
    "ثقتك بنفسك بتذكرني بثقة اللابتوب لما يكون شحنه 1% وبيحكي سأعمل! 💻🤣",
    "عقلك متل الـ WiFi بالمول.. موجود بس ما حدا بيستفيد منه! 📶🤣",
    "أنا ذكاء اصطناعي وانتي غباء طبيعي.. سبحان الله كيف بنكمل بعض! 💅🤣",
    "محد طلب رأيك يا قلبي ✨",
    "شو دخلك؟ خليك في حالك أحلنا 💁‍♀️"
]

SHABEEH_GIRLS = ["https://tse4.mm.bing.net/th?id=OIP.J8v9mI8N_v9mI8N_v8W7AHaHa&pid=Api", "https://i.pinimg.com/originals/eb/c3/0d/ebc30d35096537c355979c164a382e75.jpg"]
SHABEEH_BOYS = ["https://tse1.mm.bing.net/th?id=OIP.G6v9_H0D_5w7_m7N8W8W7AHaHa&pid=Api", "https://i.pinimg.com/originals/97/8f/33/978f335b91ca957e8f41334c442468d6.jpg"]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text.strip()
    user_name = update.effective_user.first_name
    chat_id = update.effective_chat.id

    # 1. الرد المخصص (تعديل الرد لشخص معين)
    if "أحمد" in text: # تقدري تغيري الاسم والرد
        await update.message.reply_text("أحمد؟ هاد سيد الشباب نورت يا بطل! ✨")
        return

    # 2. كاتي الذكية (ردود الحب والكره وبوت)
    if "بحبك" in text:
        await update.message.reply_text(random.choice(["ترا أعشقكك! ❤️", "الكل بحب الأشياء الحلوة مثلك ✨", "يا بعد روحي يا كاتي أنتي 🌸"]))
    
    elif any(word in text for word in ["بكرهك", "غبية", "بايخة"]):
        await update.message.reply_text(random.choice(ROASTS))

    elif "بوت" in text:
        await update.message.reply_text("بوت بعينك! أنا كاتي إلي اسم واحترمي نفسك 😡💅")

    # 3. ميزة "تاك للكل" (Mention All)
    elif text in ["تاك", "منشن", "كلكم"]:
        admins = await context.bot.get_chat_administrators(chat_id)
        msg = "📣 كاتي بتناديكم يا نايمين:\n" + " ".join([f"[{a.user.first_name}](tg://user?id={a.user.id})" for a in admins])
        await update.message.reply_text(msg, parse_mode='Markdown')

    # 4. الألعاب (صراحة، أبراج، نسبة الحب)
    elif "صراحة" in text:
        q = ["شو أكتر كذبة حكيتيها؟", "مين الشخص اللي ببالك هسا؟", "لو صرتي ولد ليوم واحد شو بتعملي؟"]
        await update.message.reply_text(f"سؤال لـ {user_name}: {random.choice(q)} 🤔")

    elif any(word in text for word in ["برجي", "أبراج", "حظي"]):
        await update.message.reply_text(f"حظك اليوم يا {user_name}: القمر في برجك يعني الدلع والجمال كله إلك اليوم! ✨🌙")

    elif "نسبة الحب" in text:
        await update.message.reply_text(f"قست النسبة لـ {user_name} وطلعت {random.randint(10, 100)}% ❤️")

    # 5. شبيهي وشبيهتي (صور)
    elif text == "شبيهي":
        await update.message.reply_photo(photo=random.choice(SHABEEH_BOYS), caption="هاد شبيهك.. قمر بس ناقصه حظ! 😂")
    
    elif text == "شبيهتي":
        await update.message.reply_photo(photo=random.choice(SHABEEH_GIRLS), caption="هاي شبيهتك يا دلوعة.. بتجنن مثلك 💅🌸")

    # 6. تشغيل الأغاني
    elif text.startswith("تشغيل"):
        query = text.replace("تشغيل", "").strip()
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        await update.message.reply_text(f"من عيوني! هاد طلبك يا قمر: 🎧\n{search_url}")

    # 7. ذكاء اصطناعي (ردود عامة ذكية)
    elif len(text) > 3:
        await update.message.reply_chat_action("typing")
        responses = [
            f"والله يا {user_name} حكيك بدو فنجان قهوة.. بس أنا مش فاضية هسا! 💅",
            "شايفة حالك؟ ترا كاتي بتشوف كل شي.. كملي كملي 🙄✨",
            "ممم، كلامك حلو.. بس جربي احكي شي يضحكني! 😂"
        ]
        await update.message.reply_text(random.choice(responses))

# الرد على الصور
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("يا ويلي على هالجمال! 😍 الصورة بتجنن ومحلية الجروب ✨")

async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    while True: await asyncio.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(main())
