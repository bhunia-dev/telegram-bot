from telegram.ext import ApplicationBuilder, MessageHandler, filters

# Your Telegram Bot API Token
TOKEN = "8827531750:AAH_0sxgVeMag0X_VMY_ySaykkMoGihD2Kw"

async def handle(update, context):
    user_text = update.message.text
    await update.message.reply_text(f"You said: {user_text}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))

app.run_polling()