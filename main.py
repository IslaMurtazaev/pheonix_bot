import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

TELEGRAM_KEY = os.getenv('TELEGRAM_KEY')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'I hope you know what you are getting into {update.effective_user.first_name}')


async def track(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Good luck')


async def complete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Woohoo good job!')

app = ApplicationBuilder().token(TELEGRAM_KEY).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
