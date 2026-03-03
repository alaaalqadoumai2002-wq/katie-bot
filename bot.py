import os
import random
import asyncio
import threading
import urllib.parse
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- إعداد Flask للبقاء حياً على Render ---
app = Flask(__name__)
@app.route('/')
def health_check(): return "Katie is the Queen! 👑", 200

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

# --- التوكن الخاص بكِ ---
TOKEN = "8423220635:AAH4TLlf4MZunC63X-oGMQDPohtyaNKnO28"

# --- قاعدة بيانات الردود (تقدري تضيفي أسماء صاحباتك وردودهم هنا) ---
CUSTOM_RESPONSES = {
    "أحمد": "أومج! أحمد هاد المنور الجروب كله؟ أهلاً يا بطل! ✨",
    "سارة": "سارة؟ هاي الحب والقلب، نورتي يا قمر الجروب 🌸",
    "بوت": "بوت في عينك! أنا كاتي، الدلوعة والذكية، احترمي حالك 💅😡"
}

ROASTS = [
    "وجهك ولا وجه علبة سردين مطعوجة؟ 😂",
    "ثقتك بنفسك بتذكرني بثقة اللابتوب لما يكون شحنه 1% وبيحكي سأعمل! 💻🤣",
    "أنا ذكاء اصطناعي وانتي غباء طبيعي.. سبحان الله كيف بنكمل بعض! 💅🤣",
    "لا تكثري حكي، وجهك بدو فورمات من كتر ما هو معلق! 🛠️😂",
    "محد طلب رأيك يا قلبي، خليكي في حالك أحلنا ✨"
]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text.strip()
    user_name = update.effective_user.first_name
    chat_id = update.effective_chat.id

    # 1. نظام الردود المخصصة (إضافة رد لناس)
    for name, response in CUSTOM_RESPONSES.items():
        if name in text:
            await update.message.reply_text(response)
            return

    # 2. نظام تشغيل الأغاني (رابط ذكي)
    if text.startswith("تشغيل"):
        query = text.replace("تشغيل", "").strip()
        if not query:
            await update.message.reply_text("شو بدك أشغل؟ قولي (تشغيل + اسم الأغنية) يا قمر 🎧")
            return
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        await update.message.reply_text(f"من عيوني! طلبتي {query}؟ أبشري هاد طلبك: 🎧\n{url}")
        return

    # 3. نظام المنشن (تاك للكل)
    if text in ["تاك", "منشن", "كلكم"]:
        admins = await context.bot.get_chat_administrators(chat_id)
        msg = "📣 كاتي بتناديكم يا نايمين، وينكم؟:\n" + " ".join([f"[{a.user.first_name}](tg://user?id={a.user.id})" for a in admins])
        await update.message.reply_text(msg, parse_mode='Markdown')
        return

    # 4. الألعاب (صراحة، نسبة الحب، حظك)
    if "صراحة" in text:
        questions = ["شو أكتر شي بتكرهيه بنفسك؟", "مين أكتر شخص بتحبيه بالجروب؟", "شو أكبر كذبة حكيتيها؟"]
        await update.message.reply_text(f"سؤال صراحة لـ {user_name}: {random.choice(questions)} 🤔")
        return

    if "نسبة الحب" in text:
        score = random.randint(1, 100)
        await update.message.reply_text(f"نسبة الحب عند {user_name} هي {score}% ❤️")
        return

    # 5. الذكاء العشوائي (الدردشة)
    if any(word in text.lower() for word in ["بحبك", "عسل", "كاتي"]):
        await update.message.reply_text(random.choice(["ترا أعشقكك! ❤️", "يا روحي أنتي، كاتي بتموت فيكي ✨", "تسلمي يا ذوق، كلك حلا 🌸"]))
        return

    if any(word in text.lower() for word in ["بكرهك", "غبية", "بايخة"]):
        await update.message.reply_text(random.choice(ROASTS))
        return

    # ردود دردشة ذكية ومنوعة عشان ما تكرر نفسها
    if len(text) > 2:
        await update.message.reply_chat_action("typing")
        replies = [
            f"والله يا {user_name} كلامك بدو صفنة.. بس حبيته! ✨",
            "كملي كملي، أنا كاتي وعم اسمعك بكل اهتمام 🌸",
            "ترا أنا أذكى بوت بتشوفيه، لا تحاولي تختبريني 😉💅",
            "حبيبتي انتي وكلامك عسل مثلك! 💋",
            "يا عيني عالرواق! شو رأيك نلعب أحسن؟ 🤔"
        ]
        await update.message.reply_text(random.choice(replies))

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
