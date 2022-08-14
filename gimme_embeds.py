"""
Embeds here we come!
"""
import os
import logging
import re
from dotenv import load_dotenv
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from telegram import Update

load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

# Use variables derived from custom API methods.
updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    """
    This function sets up the /start action to let the user know the
    bot is alive and ready to go.
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello")


def edit_text(text):
    """
    This function edits the text of the message, by replacing some
    website URLs with their *x counterparts that support embeds.
    """

    new_url = None

    # Setup conditionals.
    # For Twitter
    if re.search(
        r"(?P<url>twitter.com/(.*?)/[^\s]+)", text, re.IGNORECASE
    ) and not re.search(r"(?P<url>xtwitter.com[^\s]+)", text, re.IGNORECASE):
        # Isolate the Twitter URL.
        twitter_url = str(
            re.search(
                r"(?P<url>([^\s]*?)twitter.com[^\s]+)", text, re.IGNORECASE
            ).group("url")
        )
        insensitive_twitter = re.compile(re.escape("twitter.com"), re.IGNORECASE)
        new_url = insensitive_twitter.sub("vxtwitter.com", twitter_url)
        new_url = new_url.split("?")[0]  # Remove trackers

    # For TikTok
    elif re.search(
        r"(?P<url>tiktok.com/t/[^\s]+)", text, re.IGNORECASE
    ) and not re.search(r"(?P<url>xtiktok.com[^\s]+)", text, re.IGNORECASE):
        # Isolate the tiktok URL.
        tiktok_url = str(
            re.search(r"(?P<url>([^\s]*?)tiktok[^\s]+)", text, re.IGNORECASE).group(
                "url"
            )
        )
        insensitive_tiktok = re.compile(re.escape("tiktok.com"), re.IGNORECASE)
        new_url = insensitive_tiktok.sub("vxtiktok.com", tiktok_url)

    return new_url


def text_handler(update, context: CallbackContext):
    """
    The primary handler that does all the replacement action through
    the API.
    """

    # Use variables derived from custom API methods.
    message = update.message.text
    reply = update.message.reply_text

    # Check if the text contains an hyperlink and if isn't None.
    # If it contains an hyperlink, extract the URL and pass it to edit_text.
    # If it doesn't, send the entire text to edit_text.

    hyperlink_url = update.message.entities[0].url

    if hyperlink_url is None:
        reply_url = edit_text(message)
        if reply_url is not None:
            reply(reply_url)
    else:
        reply_url = edit_text(hyperlink_url)
        if reply_url is not None:
            reply(reply_url)


start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)
message_handler = MessageHandler(
    (Filters.entity("url") | Filters.entity("text_link")), text_handler
)
dispatcher.add_handler(message_handler)

updater.start_polling()
