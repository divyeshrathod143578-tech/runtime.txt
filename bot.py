from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes


TOKEN = "8624130041:AAH6rMNRRL7EzHynkiIXFkUQTPhSaAG2TSo"


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 DEMO", callback_data="demo")],
        [InlineKeyboardButton("💰 PRICE LIST", callback_data="price")],
        [InlineKeyboardButton("📞 CONTACT", callback_data="contact")]
    ])


def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back", callback_data="back")]
    ])


def price_back():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back", callback_data="price")]
    ])


def price_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("₹60 - 399 Videos", callback_data="pay_60")],
        [InlineKeyboardButton("₹89 - 499 Videos", callback_data="pay_89")],
        [InlineKeyboardButton("₹99 - 799 Videos", callback_data="pay_99")],
        [InlineKeyboardButton("₹130 - 1199 Videos", callback_data="pay_130")],
        [InlineKeyboardButton("₹149 - 2500 Group", callback_data="pay_149")],
        [InlineKeyboardButton("₹199 - 7999 Group", callback_data="pay_199")],
        [InlineKeyboardButton("₹249 - 14999 Group", callback_data="pay_249")],
        [InlineKeyboardButton("₹349 - Long Videos", callback_data="pay_349")],
        [InlineKeyboardButton("₹400 - Unlimited", callback_data="pay_400")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🎬 Welcome!\n\nChoose an option:",
        reply_markup=main_menu()
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()


    if query.data == "price":

        await query.message.delete()

        await query.message.reply_text(
            "💰 PRICE LIST\n\nSelect your plan:",
            reply_markup=price_buttons()
        )


    elif query.data.startswith("pay_"):

        await query.message.delete()

        await query.message.reply_photo(
            photo=open("qr.jpg", "rb"),
            caption="💳 Payment QR\n\nComplete payment.",
            reply_markup=price_back()
        )


    elif query.data == "price":

        pass


    elif query.data == "back":

        await query.message.delete()

        await query.message.reply_text(
            "🎬 Welcome!\n\nChoose an option:",
            reply_markup=main_menu()
        )


    elif query.data == "demo":

        await query.message.delete()

        await query.message.reply_text(
            "🎬 DEMO",
            reply_markup=back_menu()
        )


    elif query.data == "contact":

        await query.message.delete()

        await query.message.reply_text(
            "📞 Contact: @yourusername",
            reply_markup=back_menu()
        )


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()