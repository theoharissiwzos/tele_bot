import openai
import telegram
from telegram.ext import Updater, MessageHandler, Filters
import logging

# Replace "YOUR-API-KEY" with your own API key
openai.api_key = "API KEY"

# Create a new bot using the API key and token you obtained earlier
bot = telegram.Bot(" TELEGRAM BOT TOKEN")

# Set up the bot to listen for messages
updater = Updater(" TELEGRAM BOT TOKEN", use_context=True)
dispatcher = updater.dispatcher

# Define a function that generates a response to a user message using GPT-3
def generate_response(message):
    model_engine = "text-davinci-002"
    prompt = (f"{message}\n"
             )
    completions = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=1024, n=1,stop=None,temperature=0.5)
    message = completions.choices[0].text
    return message


# Define a function that will be called when the bot receives a message
def message_handler(update, context):
    print("this is update------->",update)  # <-- add this line
    print(type(update))  # <-- add this line
    # Get the user's message
    message = update.message.text
    # Generate a response using GPT-3
    response = generate_response(message)
    # Send the response to the user
    context.bot.send_message(chat_id=update.message.chat_id, text=response)


# Set the bot to call the message_handler function when it receives a message
message_handler = MessageHandler(Filters.text, message_handler)
dispatcher.add_handler(message_handler)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define an error handler function
def error_handler(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

# Set the bot to call the error_handler function when it encounters an error
dispatcher.add_error_handler(error_handler)

# Start the bot
updater.start_polling()
