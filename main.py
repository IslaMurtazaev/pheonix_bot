import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from database_utils import create_user, creat_tasks, setup_database, get_today_tasks

load_dotenv()

TELEGRAM_KEY = os.getenv('TELEGRAM_KEY')

setup_database()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    create_user(update.effective_user)
    await update.message.reply_text(f'I hope you know what you are getting into {update.effective_user.first_name}')


async def track(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Example input:
    /track
    task 1
    task 2
    """
    creat_tasks(update.message)
    await update.message.reply_text(f'Good luck')


async def complete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    get_today_tasks()
    await update.message.reply_text(f'Woohoo good job!')

app = ApplicationBuilder().token(TELEGRAM_KEY).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("track", track))
app.add_handler(CommandHandler("complete", complete))

app.run_polling()
