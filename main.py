import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

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
    tasks = get_today_tasks()
    keyboard = []
    for task in tasks:
        keyboard.append([InlineKeyboardButton(task[3], callback_data="Хорошая работа")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f'Woohoo good job!', reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    await query.answer()

    await query.edit_message_text(text=f" {query.data}")


app = ApplicationBuilder().token(TELEGRAM_KEY).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("track", track))
app.add_handler(CommandHandler("complete", complete))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
