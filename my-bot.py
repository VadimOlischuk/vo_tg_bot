import logging
import json


from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    Filters
)


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def read_env_params():
    ENV_PATH = ".env"
    data = ""
    with open(ENV_PATH, "r") as f:
        for line in f:
            data += line
    return json.loads(data)

def main() -> None:
    params = read_env_params()

ENV_FILE = ".env"

ASK_NAME, SEND_JOKE = range(2)

def start(update: Update, context) -> int:
    user = update.message.from_user
    logger.info("Start bot for user %s, with username %s and lang code %s",
                user.first_name, user.username, user.language_code)
    update.message.reply_text("Hello! What is your name?")
    return ASK_NAME

def got_name(update: Update, context) -> int:
    user = update.message.from_user.username
    message = update.message.text
    logger.info("Ask bio for user %s, got %s", user, message)
    update.message.reply_text(
        'If you want to get a joke about IT from me, write /ITjoke'
    )
    return SEND_JOKE


def get_joke(update: Update, context) -> int:


    import requests

    r = requests.get('https://geek-jokes.sameerkumar.website/api?format=json'.format(json))
    if r.status_code != 200:
        update.message.reply_text("Problems with your request, try later")
        return ConversationHandler.END

    joke = r.text

    json.loads(r.content)

    report = json.loads(r.content)

    update.message.reply_text ('{}'.format(joke))
    update.message.reply_text(
        'Do you want another joke? Write /ITjoke'
    )
    return SEND_JOKE

    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user.username
    logger.info("User % canceled the conversation.", user)
    return ConversationHandler.END


def run_bot(api_token):
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    updater = Updater(api_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(Filters.text, got_name)],
            SEND_JOKE: [MessageHandler(Filters.text, get_joke), CommandHandler('ITjoke', get_joke)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


def parse_env_params() -> dict:
    data = ""
    with open(ENV_FILE, "r") as f:
        for line in f:
            data += line
    return json.loads(data)


def main():
    env_params = parse_env_params()
    run_bot(env_params["API_KEY"])


if __name__ == "__main__":
    main()
