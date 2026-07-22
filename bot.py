import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== BOT TOKEN (Change this) ======
TOKEN = "8624130041:AAH6rMNRRL7EzHynkiIXFkUQTPhSaAG2TS0"

# ====== MAIN MENU ======
def main_menu():
    keyboard = [
        [InlineKeyboardButton("🎬 DEMO", callback_data="demo")],
        [InlineKeyboardButton("💰 PRICE LIST", callback_data="price")],
        [InlineKeyboardButton("📞 CONTACT", callback_data="contact")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== BACK BUTTON ======
def back_menu():
    keyboard = [
        [InlineKeyboardButton("🔙 BACK", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== PRICE LIST ======
def price_buttons():
    keyboard = [
        [InlineKeyboardButton("₮60 - 399 Videos", callback_data="pay_60")],
        [InlineKeyboardButton("₮89 - 499 Videos", callback_data="pay_89")],
        [InlineKeyboardButton("₮99 - 799 Videos", callback_data="pay_99")],
        [InlineKeyboardButton("₮130 - 1199 Videos", callback_data="pay_130")],
        [InlineKeyboardButton("₮149 - 2500 Group", callback_data="pay_149")],
        [InlineKeyboardButton("₮199 - 7999 Group", callback_data="pay_199")],
        [InlineKeyboardButton("₮249 - 14999 Group", callback_data="pay_249")],
        [InlineKeyboardButton("₮349 - Long Videos", callback_data="pay_349")],
        [InlineKeyboardButton("₮480 - Unlimited", callback_data="pay_480")],
        [InlineKeyboardButton("🔙 BACK", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== PRICE BACK BUTTON ======
def price_back():
    keyboard = [
        [InlineKeyboardButton("🔙 BACK TO PRICES", callback_data="price")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== START COMMAND ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = f"👋 Welcome {user.first_name}!\n\nChoose an option below:"
    await update.message.reply_text(welcome_text, reply_markup=main_menu())

# ====== BUTTON HANDLER ======
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # ----- PRICE LIST -----
    if query.data == "price":
        await query.message.edit_text(
            "💰 PRICE LIST\n\nSelect your plan:",
            reply_markup=price_buttons()
        )
    
    # ----- PAYMENT OPTIONS -----
    elif query.data.startswith("pay_"):
        plans = {
            "pay_60": "₮60 - 399 Videos",
            "pay_89": "₮89 - 499 Videos",
            "pay_99": "₮99 - 799 Videos",
            "pay_130": "₮130 - 1199 Videos",
            "pay_149": "₮149 - 2500 Group",
            "pay_199": "₮199 - 7999 Group",
            "pay_249": "₮249 - 14999 Group",
            "pay_349": "₮349 - Long Videos",
            "pay_480": "₮480 - Unlimited"
        }
        selected_plan = plans.get(query.data, "Selected Plan")
        
        try:
            # Try to send QR code image
            await query.message.delete()
            with open("qr.jpg", "rb") as qr_file:
                await query.message.reply_photo(
                    photo=qr_file,
                    caption=f"💳 Payment for: {selected_plan}\n\nScan QR code to complete payment.",
                    reply_markup=price_back()
                )
        except FileNotFoundError:
            # If QR image not found
            await query.message.edit_text(
                f"💳 {selected_plan}\n\n📞 Contact @yourusername for payment details.",
                reply_markup=price_back()
            )
    
    # ----- BACK BUTTON -----
    elif query.data == "back":
        await query.message.edit_text(
            "👋 Welcome back!\n\nChoose an option:",
            reply_markup=main_menu()
        )
    
    # ----- DEMO -----
    elif query.data == "demo":
        await query.message.edit_text(
            "🎬 DEMO\n\nThis bot provides video group services.\n\n• Multiple plans available\n• Secure payment\n• 24/7 support",
            reply_markup=back_menu()
        )
    
    # ----- CONTACT -----
    elif query.data == "contact":
        await query.message.edit_text(
            "📞 CONTACT US\n\n📱 Telegram: @yourusername\n📧 Email: support@example.com\n⏰ Response: Within 1 hour",
            reply_markup=back_menu()
        )
    
    # ----- UNKNOWN -----
    else:
        await query.message.edit_text(
            "❌ Invalid option. Please try again.",
            reply_markup=main_menu()
        )

# ====== MAIN FUNCTION ======
def main():
    print("🤖 Bot is starting...")
    
    # Create application
    app = Application.builder().token(TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # Start bot
    print("✅ Bot is running! Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
