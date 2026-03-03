import os
import random
import asyncio
import threading
import urllib.parse
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

app = Flask(__name__)
@app.route('/')
def health_check(): return "Katie is Savage! 💅", 200

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

TOKEN = "8423220635:AAH4TLlf4MZunC63X-oGMQDPohtyaNKnO28"

# --- داتا القصف والمشاكل ---
SAVAGE_ROASTS = [
    "وجهك ولا وجه علبة سردين مطعوجة؟ 😂",
    "ثقتك بنفسك بتذكرني بثقة اللابتوب لما يكون شحنه 1% وبيحكي سأعمل! 💻🤣",
    "لو الغباء بيوجع، كان الجيران اشتكوا من صوت صراخك! 🙄😂",
    "عقلك متل الـ WiFi بالمول.. موجود بس ما حدا بيستفيد منه! 📶🤣",
    "أنا ذكاء اصطناعي وانتي غباء طبيعي.. سبحان الله كيف بنكمل بعض! 💅🤣",
    "لا تكثري حكي، وجهك بدو فورمات من كتر ما هو معلق! 🛠️😂"
]

# --- داتا الصور ---
SHABEEH_BOYS = ["https://tse1.mm.bing.net/th?id=OIP.G6v9_H0D_5w7_m7N8W8W7AHaHa&pid=Api"]
SHABEEH_GIRLS = ["https://tse4.mm.bing.net/th?id=OIP.J8v9mI8N_v9mI8N_v8W7AHaHa&pid=Api"]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text.lower()
    user_name = update.effective_user.first_name
    chat_id = update.effective_chat.id

    # 1. قسم القصف والمشاكل (لما حدا يغلط أو يستفزها)
    if any(word in text for word in ["بايخة", "غبية", "هبلة", "دبة", "انقلعي", "اسكتي"]):
        await update.message.reply_text(f"اسمعي يا {user_name}.. {random.choice(SAVAGE_ROASTS)}")
        return

    elif "بوت" in text:
        await update.message.reply_text("بوت بعينك! أنا كاتي ست البنات، روحي شوفي وجهك بالمراية بالأول! 😡💅")
        return

    # 2. ردود الحب والدلع
    elif "بحبك" in text:
        await update.message.reply_text(random.choice(["ترا أعشقكك! ❤️", "الكل بحب الأشياء الحلوة مثلك ✨", "يا بعد روحي أنتي! 🌸"]))
        return

    # 3. ميزة "تاك للكل"
    elif text in ["تاك", "منشن"]:
        admins = await context.bot.get_chat_administrators(chat_id)
        msg = "📣 كاتي بتناديكم يا نايمين:\n" + " ".join([f"[{a.user.first_name}](tg://user?id={a.user.id})" for a in admins])
        await update.message.reply_text(msg, parse_mode='Markdown')
        return

    # 4. الألعاب (صراحة، أبراج، اعتراف)
    elif "صراحة" in text:
        q = ["شو أكتر كذبة حكيتيها؟", "مين الشخص اللي مقهورة منه؟", "لو صرتي ولد ليوم واحد شو بتعملي؟"]
        await update.message.reply_text(f"سؤال صراحة لـ {user_name}: {random.choice(q)} 🤔")
        return

    elif "برجي" in text or "أبراج" in text:
        await update.message.reply_text(f"برجك اليوم يا {user_name}: في قصف جبهات قادم لكِ بالطريق، انتبهي من كاتي! 😂🌙")
        return

    # 5. شبيهي وشبيهتي
    elif text == "شبيهي":
        await update.message.reply_photo(photo=random.choice(SHABEEH_BOYS), caption="هاد شبيهك.. بيشبهك وانتي معصبة! 😂")
        return
    elif text == "شبيهتي":
        await update.message.reply_photo(photo=random.choice(SHABEEH_GIRLS), caption="هاي شبيهتك.. قمر مثلك بس ناقصك شوية عقل! 💅🌸")
        return

    # 6. الذكاء الاصطناعي (ردود عامة)
    else:
        if len(text) > 3:
            responses = [
                f"والله يا {user_name} حكيك بدو فنجان قهوة وروقان.. بس أنا مش فاضية هسا! ☕💅",
                "شايفة حالك؟ ترا كاتي بتشوف كل شي.. كملي كملي 🙄✨",
                "كلامك حلو.. بس جربي احكي شي يضحكني بدل النكد! 😂",
                "ممم، ذكاء اصطناعي وأنوثة طاغية.. شو بدك أكتر من هيك؟ 👑"
            ]
            await update.message.reply_text(random.choice(responses))

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("يا ويلي على هالجمال! 😍 الصورة بتجنن بس لا تشوفي حالك علينا ✨")

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
