# Existing Imports
import datetime
import json
import os

import discord
import dotenv

# customer imports
from alfred import AlfredChat
from api.coin import CoinInfo
from dbhandler import DBHandler
from log import setup_logger

# Initialize the database
db_handler = DBHandler('alfred_database.db')

# Initialize Global Variable
alfred_instances = []
api_key = os.environ.get("OPENAI_API_KEY")


# Function to Create New Instance
def create_new_instance(engine="text-davinci-003", tokens=300):
    global alfred_instances
    new_instance = AlfredChat(engine=engine, tokens=tokens)
    alfred_instances.append(new_instance)
    return new_instance


# Function to Clear All Instances
def clear_all_instances():
    global alfred_instances
    alfred_instances.clear()


# Existing Discord Logic
dotenv.load_dotenv()
logger = setup_logger()
intents = discord.Intents.default()
intents.message_content = True
DISCORD_APP_TOKEN = os.getenv("DISCORD_APP_TOKEN")

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    global alfred_instances  # Access the global variable
    logger.info(f"We have logged in as {client.user}. Number of Alfred instances: {len(alfred_instances)}")


# Users code
users = {}
try:
    with open('./data/users.json', 'r') as f:
        users = json.load(f)
except FileNotFoundError:
    logger.info("No existing users found, creating new users dictionary.")
    users = {}


async def save_users():
    with open('./data/users.json', 'w') as f:
        json.dump(users, f)


# Conversations
ongoing_conversations = []


async def track_convo(sender, message):
    global ongoing_conversations
    ongoing_conversations.append({"sender": sender, "message": message})
    print("OG:", ongoing_conversations)


# This function returns a simplified string context for the conversation of a given userID
def get_simple_context():
    conversation = json.dumps(ongoing_conversations)
    # print("DEBUG: conversation", conversation)
    simple_context = "Context to conversation:\n"

    for i in ongoing_conversations:
        simple_context += i["sender"] + ": " + i["message"] + "\n"

    print("DEBUG: simple_context", simple_context)

    return simple_context


async def handle_user_profile(message, db_handler, logger):
    user_id = str(message.author.id)
    existing_user = db_handler.get_user_by_id(user_id)
    if not existing_user:
        logger.info(f"Creating new profile for {message.author.name}")
        current_time = str(
            datetime.datetime.now())  # Assuming you want to use the current time as the LastActive timestamp
        db_handler.create_user(user_id, message.author.name, current_time, 0)


async def handle_alfred_chat(message, users, logger, api_key, ongoing_conversations):
    user_id = str(message.author.id)
    # ongoing_conversations[user_id] = {"messages": []}

    prompt = message.content[1:]

    # Track the user's message
    # await track_convo(user_id, prompt, "User")

    alfred = AlfredChat(api_key)
    res = alfred.return_completion(prompt)
    await track_convo("alfred", res)
    reply = await message.reply(res)

    # Track Alfred's message
    # await track_convo(user_id, res, "Alfred")

    logger.info(f"Sent reply: {res}")


async def handle_replies(message, logger, api_key, ongoing_conversations):
    # Extract the user_id from the message author
    user_id = str(message.author.id)
    await track_convo(user_id, message.content)
    context = get_simple_context()
    alfred = AlfredChat(api_key)
    res = alfred.return_completion(prompt=context)
    await track_convo("alfred", res)
    reply = await message.reply(res[8:])


async def handle_coin_price(message, logger):
    await message.channel.send('coin price requested')
    symbol = message.content[6:].strip()
    logger.info(f"Coin price requested for {symbol if symbol else 'bitcoin'}")
    coin = CoinInfo(symbol if symbol else 'bitcoin')
    await message.channel.send(coin.get_price())


async def handle_help_command(message, logger):
    help_commands = {
        'greet': 'Say hello to the bot.',
        'bye': 'Say goodbye to the bot.',
        'weather': 'Get current weather information.',
        'help': 'List all available commands.'
    }

    help_text = "Available commands:\n"
    for cmd, description in help_commands.items():
        help_text += f"{cmd}: {description}\n"

    await message.channel.send(help_text)
    logger.info(f"Help requested by {message.author.name}")


@client.event
async def on_message(message):
    user_id = str(message.author.id)  # Discord User ID
    user_message = message.content  # Message from the user

    global db_handler  # Assuming db_handler is a global variable

    if message.author == client.user:
        return

    await handle_user_profile(message, db_handler, logger)

    if message.content.startswith('!'):
        ongoing_conversations.clear()
        await handle_alfred_chat(message, db_handler, logger, api_key, ongoing_conversations)
        # await track_convo(user_id, user_message, "User")

    elif message.reference:
        await handle_replies(message, logger, api_key, ongoing_conversations)
        # await track_convo(user_id, user_message, "User")

    elif message.content.startswith('&'):
        if message.content[:5] == '&coin':
            await handle_coin_price(message, logger)
        elif message.content[:5] == '&help':
            await handle_help_command(message, logger)
        elif message.content == '&select *':
            await DBHandler.handle_database_dump(message, db_handler)
        # await track_convo(user_id, user_message, "User")

    # Tracking the conversation for both Alfred and the User
    # await track_convo(user_id, user_message, "User")

    # To get the conversation context
    context = get_simple_context()
    print(ongoing_conversations)


client.run(DISCORD_APP_TOKEN)
