from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

TOKEN = "8099048540:AAHhM8KPnThNX2TVVXk8KFXrpTFCJU4eNmo"

def start(update, context):
    welcome_message = """🏠 Hi Imam:

🎙 Sampling audios and converting to voice
😊 Adding custom reaction buttons (👍👎👏) to you messages,
😊 Write HTML text messages,
🤔 Change caption of audios, videos, photos..., and remove ads, no need to upload and download again,
📎 Attach inline URL buttons to your messages,

⭐️ Send me a photo/misic/message to continue..."""

    update.message.reply_text(
        welcome_message,
        parse_mode=ParseMode.HTML
    )
    
    # Tambahkan tombol setelah pesan selamat datang
    add_button(update, context)

def add_button(update, context):
    keyboard = [
        [InlineKeyboardButton("Add url button", callback_data='add_url')],
        [InlineKeyboardButton("Publish", callback_data='publish')],
        [InlineKeyboardButton("Publish to channel", callback_data='publish_channel')],
        [InlineKeyboardButton("Publish to channel (silent)", callback_data='publish_silent')],
        [InlineKeyboardButton("Parse as HTML", callback_data='parse_html')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Pilih opsi:', reply_markup=reply_markup)

def button_callback(update, context):
    query = update.callback_query
    query.answer()
    
    if query.data == 'add_url':
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Kirim format tombol URL dengan format:\ntext_tombol|url"
        )
    
    elif query.data == 'publish':
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Pesan telah dipublikasikan!"
        )
    
    elif query.data == 'publish_channel':
        context.bot.send_message(
            chat_id="@nama_channel",
            text="Pesan untuk channel"
        )
    
    elif query.data == 'publish_silent':
        context.bot.send_message(
            chat_id="@nama_channel",
            text="Pesan untuk channel",
            disable_notification=True
        )
    
    elif query.data == 'parse_html':
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="<b>Teks Bold</b>\n<i>Teks Italic</i>",
            parse_mode=ParseMode.HTML
        )

def handle_text(update, context):
    text = update.message.text
    if "|" in text:
        try:
            button_text, url = text.split("|")
            keyboard = [[InlineKeyboardButton(button_text.strip(), url=url.strip())]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text("Preview tombol:", reply_markup=reply_markup)
        except Exception as e:
            update.message.reply_text("Format tidak valid! Gunakan: text_tombol|url")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Handler untuk command /start
    dp.add_handler(CommandHandler("start", start))
    
    # Handler untuk callback tombol
    dp.add_handler(CallbackQueryHandler(button_callback))
    
    # Handler untuk pesan teks
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
