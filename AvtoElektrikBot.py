from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("8210806536", "0"))
XIZMATLAR = [
    "🔌 Sim va elektr tizimini ta'mirlash",
    "⚙️ Starter va generator",
    "💡 Chiroqlar va faralar",
    "🔐 Signalizatsiya va markaziy qulf",
    "🖥️ Kompyuter diagnostikasi (OBD2)",
    "⚡ Elektr tizimini tekshirish",
    "🔑 Mashina eshigini ochish",
    "🛠 Boshqa xizmatlar",
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    keyboard = [[x] for x in XIZMATLAR]

    await update.message.reply_text(
        "🚗 AVTO ELEKTRIK\n"
        "📍 Navoiy shahri\n"
        "🚘 Chaqiruv bo'yicha xizmat\n\n"
        "Kerakli xizmatni tanlang:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True
        ),
    )


async def id_ol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Telegram ID: {update.effective_user.id}"
    )


async def bekor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Buyurtma bekor qilindi. Qayta boshlash uchun /start bosing."
    )


async def matn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    javob = update.message.text.strip()
    qadam = context.user_data.get("qadam")

    if javob == "🔄 Yangi buyurtma":
        context.user_data.clear()
        await start(update, context)
        return

    if not qadam:
        if javob not in XIZMATLAR:
            await update.message.reply_text(
                "Xizmatni menyudan tanlang yoki /start bosing."
            )
            return

        context.user_data["xizmat"] = javob
        context.user_data["qadam"] = "ism"
        await update.message.reply_text("👤 Ism-familiyangizni yozing:")

    elif qadam == "ism":
        context.user_data["ism"] = javob
        context.user_data["qadam"] = "telefon"
        await update.message.reply_text("📞 Telefon raqamingizni yozing:")

    elif qadam == "telefon":
        context.user_data["telefon"] = javob
        context.user_data["qadam"] = "mashina"
        await update.message.reply_text(
            "🚘 Mashina rusumi va yilini yozing.\n"
            "Masalan: Chevrolet Cobalt, 2018"
        )

    elif qadam == "mashina":
        context.user_data["mashina"] = javob
        context.user_data["qadam"] = "manzil"
        await update.message.reply_text("📍 Navoiydagi manzilingizni yozing:")

    elif qadam == "manzil":
        context.user_data["manzil"] = javob
        context.user_data["qadam"] = "muammo"
        await update.message.reply_text(
            "🛠 Muammoni tushuntiring.\n"
            "Diagnostika bo'lsa, xatolik belgilarini yozing.\n"
            "Eshik ochish xizmati bo'lsa, avtomobil sizniki "
            "yoki ochishga ruxsatingiz borligini tasdiqlang."
        )

    elif qadam == "muammo":
        buyurtma = (
            "🚗 YANGI BUYURTMA\n\n"
            f"🔧 Xizmat: {context.user_data['xizmat']}\n"
            f"👤 Ism: {context.user_data['ism']}\n"
            f"📞 Telefon: {context.user_data['telefon']}\n"
            f"🚘 Mashina: {context.user_data['mashina']}\n"
            f"📍 Manzil: {context.user_data['manzil']}\n"
            f"🛠 Muammo: {javob}\n"
            f"🆔 Telegram ID: {update.effective_user.id}"
        )

        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=buyurtma,
            )
        except Exception as e:
            print(f"Buyurtma yuborilmadi: {e}")
            await update.message.reply_text(
                "❌ Buyurtma yuborilmadi. Admin ID va botga /start "
                "yuborilganini tekshiring."
            )
            return

        context.user_data.clear()
        await update.message.reply_text(
            "✅ Buyurtmangiz ustaga yuborildi!",
            reply_markup=ReplyKeyboardMarkup(
                [["🔄 Yangi buyurtma"]],
                resize_keyboard=True,
            ),
        )


def main():
    if BOT_TOKEN == "BU_YERGA_BOTFATHER_TOKENINGNI_QOY":
        raise RuntimeError("BotFather tokenini kodga kiriting!")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", id_ol))
    app.add_handler(CommandHandler("cancel", bekor))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, matn)
    )

    print("Avto Elektrik bot ishga tushdi!")
    app.run_polling()


if __name__ == "__main__":
    main()
