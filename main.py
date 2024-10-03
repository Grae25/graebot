from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import threading

app = Flask(__name__)

# Function to handle the start command and display the options
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Spiel Spielen", callback_data='play_game')],
        [InlineKeyboardButton("Spaß Fakt", callback_data='get_fun_fact')],
        [InlineKeyboardButton("Witz Bekommen", callback_data='get_joke')],
        [InlineKeyboardButton("Promo", callback_data='send_promo')],
        [InlineKeyboardButton("Quiz", callback_data='send_quiz')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Willkommen! Wählen Sie eine Option:', reply_markup=reply_markup)

# Function to handle the "Spiel Spielen" button
async def play_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    response = (
        "Das ist ein lustiges Spiel! Versuche es noch einmal.\n\n"
        "Für exklusive Inhalte, treten Sie unserem Kanal bei!"
        "\n\n[Treten Sie unserem Kanal bei](https://t.me/+C8R6wRn_VCBlZDZi)"
    )
    await query.edit_message_text(text=response, disable_web_page_preview=True)

# Function to handle the "Spaß Fakt" button
async def get_fun_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    fact = "Wussten Sie, dass das Brandenburger Tor in Berlin über 200 Jahre alt ist?"
    await query.edit_message_text(
        text=f"{fact}\n\nFür exklusive Inhalte, treten Sie unserem Kanal bei!\n\n[Treten Sie unserem Kanal bei](https://t.me/+C8R6wRn_VCBlZDZi)",
        disable_web_page_preview=True,
    )

# Function to handle the "Witz Bekommen" button
async def get_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    joke = "Warum können Geister so schlecht lügen? Weil man durch sie hindurchsehen kann!"
    await query.edit_message_text(
        text=f"{joke}\n\nFür exklusive Inhalte, treten Sie unserem Kanal bei!\n\n[Treten Sie unserem Kanal bei](https://t.me/+C8R6wRn_VCBlZDZi)",
        disable_web_page_preview=True,
    )

# Function to handle the "Promo" button
async def send_promo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    promo_message = "Exklusive Angebote nur für Mitglieder unseres Kanals!"
    await query.edit_message_text(
        text=f"{promo_message}\n\nTreten Sie unserem Kanal bei, um keine Aktion zu verpassen.\n\n[Treten Sie unserem Kanal bei](https://t.me/+C8R6wRn_VCBlZDZi)",
        disable_web_page_preview=True,
    )

# Function to handle the "Quiz" button
async def send_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quiz_question = "Was ist die Hauptstadt von Deutschland?"
    correct_answer = "Berlin"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Berlin", callback_data=f"quiz_answer_{correct_answer}")],
        [InlineKeyboardButton("München", callback_data="quiz_answer_München")],
        [InlineKeyboardButton("Hamburg", callback_data="quiz_answer_Hamburg")],
        [InlineKeyboardButton("Köln", callback_data="quiz_answer_Köln")],
    ])
    if update.callback_query:
        await update.callback_query.message.reply_text(quiz_question, reply_markup=reply_markup)
    else:
        await update.message.reply_text(quiz_question, reply_markup=reply_markup)

# Handle the quiz answer
async def handle_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    answer = query.data.split('_')[2]  # Extract the selected answer
    correct_answer = "Berlin"
    if answer == correct_answer:
        response = (
            "Richtig! Die Hauptstadt von Deutschland ist Berlin.\n\n"
            "Für weitere exklusive Inhalte, treten Sie unserem Kanal bei!"
            "\n\n[Treten Sie unserem Kanal bei](https://t.me/+C8R6wRn_VCBlZDZi)"
        )
    else:
        response = (
            f"Leider falsch. {answer} ist nicht die Hauptstadt von Deutschland.\n\n"
            "Versuche es nochmal! Für exklusive Inhalte, treten Sie unserem Kanal bei!"
            "\n\n[Treten Sie unserem Kanal bei](https://t.me/+C8R6wRn_VCBlZDZi)"
        )
    await query.edit_message_text(text=response, disable_web_page_preview=True)

# Create the Telegram bot application
telegram_app = Application.builder().token("7943387702:AAF48fmBJAFeZ8qdQJFHS8PS3n7_newSDPg").build()

# Add the handlers to the Telegram bot
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(play_game, pattern='play_game'))
telegram_app.add_handler(CallbackQueryHandler(get_fun_fact, pattern='get_fun_fact'))
telegram_app.add_handler(CallbackQueryHandler(get_joke, pattern='get_joke'))
telegram_app.add_handler(CallbackQueryHandler(send_promo, pattern='send_promo'))
telegram_app.add_handler(CallbackQueryHandler(send_quiz, pattern='send_quiz'))
telegram_app.add_handler(CallbackQueryHandler(handle_quiz_answer, pattern=r'quiz_answer_.*'))

# Flask route
@app.route('/')
def home():
    return "Hello, this is your Telegram bot running!"

# Function to run the Flask app
def run_flask():
    app.run(host='0.0.0.0', port=3000)

# Start the Flask app in a separate thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Start the Telegram bot
telegram_app.run_polling()
