import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import threading
import random

# إعداد Flask عشان Render يضل صاحي
app = Flask(__name__)
@app.route('/')
def hello(): return "Katie is Online with Wisdom!"

# رسالة الترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"يا مية هلا بـ {user_name}! 🌸 أنا كاتي.. صرت أحكي بكل اللهجات، بنلعب سوا، وبنقرأ قصص وعبر كمان! جربي قولي 'نلعب' أو 'قصة' وشوفي!")

# نظام الردود العملاق (الألعاب، العبر، اللهجات)
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user_name = update.effective_user.first_name
    
    # 1. نداء كاتي
    if any(word in text for word in ["كاتي", "يا كاتي", "وينك"]):
        await update.message.reply_text(f"هلا هلا! لبّيه يا {user_name}.. عيوني إلك 😍")

    # 2. قائمة الخدمات والألعاب
    elif any(word in text for word in ["نلعب", "لعبة", "ألعاب", "قائمة"]):
        menu = (
            "🌟 **خدمات كاتي المميزة** 🌟\n"
            "━━━━━━━━━━━━━\n"
            "📖 اكتب **'قصة'** (قصص دينية وعبر مؤثرة)\n"
            "🎲 اكتب **'حظي'** (رقم وحظك: تحدي، سؤال، حزورة)\n"
            "🔥 اكتب **'اعتراف'** (كرسي الاعتراف القوي)\n"
            "🤔 اكتب **'لو خيروك'** (حيرة وتحدي)\n"
            "🌟 اكتب **'برجي'** (حظك الفكاهي اليوم)\n"
            "😂 اكتب **'نكتة'** (فرط ضحك)\n"
            "━━━━━━━━━━━━━\n"
            "شو حابة تبدأي؟"
        )
        await update.message.reply_text(menu)

    # 3. قسم القصص والعبر (الجديد)
    elif any(word in text for word in ["قصة", "قصه", "عبرة", "عبره", "حكمة"]):
        stories = [
            "📖 **عبرة:** سأل رجل أحد الصالحين: كم أقرأ من القرآن؟ قال: على قدر السعادة التي تريدها! فكلما زاد وردك زادت سعادتك. ✨",
            "📖 **قصة:** جاء رجل للنبي ﷺ يشكو قسوة قلبه، فقال له: 'أتحب أن يلين قلبك وتدرك حاجتك؟ ارحم اليتيم وامسح رأسه وأطعمه من طعامك'. القلب يلين بالإحسان. ❤️",
            "📖 **حكمة:** سئل حكيم: لماذا لا نرى العيب في أنفسنا كما نراه في غيرنا؟ فقال: لأن الإنسان يرى غيره بعينه، ويرى نفسه بهواه، والهوى يعمي البصر! 🧐",
            "📖 **قصة قصيرة:** مر إبراهيم بن أدهم برجل حزين، فقال له: أيجري في هذا الكون شيء لا يريده الله؟ قال: لا. قال: أينقص من رزقك شيء قدره الله؟ قال: لا. قال: فلماذا الحزن إذن؟ استبشر خيراً! 🌸",
            "📖 **عبرة:** لو علمنا كيف يدبر الله لنا الأمور، لذابت قلوبنا من حبه. لا تحزن على ما فات، فقدر الله كله خير. ✨"
        ]
        await update.message.reply_text(random.choice(stories))

    # 4. لعبة برجي
    elif "برجي" in text:
        horoscopes = ["برجك اليوم: رح تضحكي من قلبك اليوم، بس لا تنسي تحمدي ربنا! 😂", "حظك: في رزقة جاية بالطريق، استعدي! 💸"]
        await update.message.reply_text(f"🔮 **حظك الفكاهي مع كاتي:** \n\n{random.choice(horoscopes)}")

    # 5. الأرقام (1-5)
    elif text in ["1", "2", "3", "4", "5"]:
        res = {"1": "🎯 تحدي: استغفري 10 مرات هسا! ❤️", "2": "❓ سؤال: شو أكثر آية قرآنية بتريح قلبك؟ ✨", "3": "🧩 حزورة: ما هو الشيء الذي لا يمشي إلا بالضرب؟ (المسمار 🔨)", "4": "🔥 اعتراف: متى كانت آخر مرة بكيتي فيها من قلبك؟ 🥺", "5": "🎁 حظك: إلك دعوة بظهر الغيب من كاتي! الله يسعدك."}
        await update.message.reply_text(res[text])

    # 6. الرد على "بوت"
    elif "بوت" in text:
        await update.message.reply_text("بوت في عينك! اسمي كاتي.. كـ ا تـ ي! 😤💅")

    # 7. اللهجات
    elif "ازيك" in text: await update.message.reply_text("زي الفل يا قشطة! إنتي عاملة إيه؟ 🇪🇬")
    elif "كيفك" in text: await update.message.reply_text("بخير والحمد لله، إنتي شو أخبارك يا غالية؟ 🇵🇸🇯🇴")

    # 8. نكت
    elif "نكتة" in text:
        await update.message.reply_text("مرة واحد غبي لقى كنز، قال: الحمد لله، بس يارب الخريطة تطلع صح! 🤣")

    # 9. الرد الافتراضي
    else:
        await update.message.reply_text(f"كلامك طيب مثلك! جربي اكتبي 'قائمة' لتشوفي كل ميزاتي 🌸")

if __name__ == "__main__":
    TOKEN = "7547648347:AAH0qR5uT8U6Y8-rL6oW3D8XqJ2Z9M1N4B0" 
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    port = int(os.environ.get('PORT', 5000))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()
    application.run_polling()
