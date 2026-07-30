from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import requests

TELEGRAM_TOKEN = "8827531750:AAH_0sxgVeMag0X_VMY_ySaykkMoGihD2Kw"
OMDB_API_KEY = "5fc58451"

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        welcome_text = f"Welcome to the group, {member.first_name}! 🎬\nমুভি খুঁজতে চাইলে টাইপ করুন: /movie মুভির_নাম"
        await update.message.reply_text(welcome_text)

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("দয়া করে মুভির নাম দিন। উদাহরণ: `/movie Inception`", parse_mode="Markdown")
        return

    movie_name = " ".join(context.args)
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    
    try:
        response = requests.get(url).json()

        if response.get("Response") == "True":
            title = response.get("Title")
            year = response.get("Year")
            plot = response.get("Plot")
            poster = response.get("Poster")
            rating = response.get("imdbRating")
            genre = response.get("Genre")

            caption = (
                f"🎬 *{title}* ({year})\n"
                f"🎭 *Genre:* {genre}\n"
                f"⭐ *IMDb Rating:* {rating}\n\n"
                f"📖 *Plot:* {plot}"
            )

            if poster and poster != "N/A":
                await update.message.reply_photo(photo=poster, caption=caption, parse_mode="Markdown")
            else:
                await update.message.reply_text(caption, parse_mode="Markdown")
        else:
            await update.message.reply_text("দুঃখিত! এই নামের কোনো মুভি খুঁজে পাওয়া যায়নি। 😔")
            
    except Exception as e:
        await update.message.reply_text("সার্ভারে কোনো সমস্যা হয়েছে। একটু পর আবার চেষ্টা করুন।")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    app.add_handler(CommandHandler("movie", search_movie))

    app.run_polling()
