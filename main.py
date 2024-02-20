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
# check if it exists first
if not os.path.exists('alfred_database.db'):
    import dbsetup

    dbsetup.setup_database()

db_handler = DBHandler('alfred_database.db')

# Initialize Global Variable
api_key = os.environ.get("OPENAI_API_KEY")

# Existing Discord Logic
dotenv.load_dotenv()
logger = setup_logger()
intents = discord.Intents.default()
intents.message_content = True
DISCORD_APP_TOKEN = os.getenv("DISCORD_APP_TOKEN")

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    # global alfred_instances  # Access the global variable
    logger.info(f"We have logged in as {client.user}.")


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


async def track_convo(sender, content):
    global ongoing_conversations
    # Assuming 'sender' is either 'user' or 'assistant'
    role = 'user' if sender != "alfred" else 'assistant'
    ongoing_conversations.append({"role": role, "content": content})
    print("OG:", ongoing_conversations)


def get_simple_context():
    # Assuming ongoing_conversations is a list of dicts with 'role' and 'content'
    simple_context = "Context of conversation:\n"
    for i in ongoing_conversations:
        role = i["role"]
        # Map 'role' to a more human-readable form if desired, e.g., 'user' to actual usernames or 'assistant' to 'Alfred'
        # This step is optional and can be customized based on your application's needs
        content = i["content"]
        simple_context += f"{role}: {content}\n"
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


async def handle_alfred_chat(message, db_handler, logger, api_key, ongoing_conversations):
    user_id = str(message.author.id)
    user_message = message.content[1:]  # Strip the command prefix to get the actual message

    # Before sending the user message to OpenAI, track it in the conversation history
    await track_convo(user_id,
                      user_message)  # Assuming 'user_id' can be mapped to 'user' or 'assistant' role appropriately within `track_convo`

    # Initialize the AlfredChat instance with the API key
    alfred = AlfredChat(api_key)

    # Pass the ongoing conversation to AlfredChat for generating the response
    # Ensure that 'ongoing_conversations' is in the correct format, as expected by the ChatCompletion API
    response_text = alfred.return_completion(ongoing_conversations)

    # After receiving the response from AlfredChat, track this response in the conversation
    await track_convo("alfred", response_text)  # This assumes "alfred" is treated as 'assistant' in `track_convo`

    # Reply to the user message with Alfred's response
    await message.reply(response_text)

    # Log the response sent for debugging or monitoring purposes
    logger.info(f"Sent reply: {response_text}")


async def handle_replies(message, logger, api_key, ongoing_conversations):
    # Check if this message is a reply
    if message.reference is not None:
        # This is a reply to a previous message
        # Extract message content
        user_message = message.content
        # Track the user's reply
        await track_convo('user', user_message)  # Assuming this function correctly appends to ongoing_conversations

        # Prepare the messages for the chat model
        alfred = AlfredChat(api_key)
        # Now call return_completion with the list of messages directly
        response_text = alfred.return_completion(ongoing_conversations)

        # Track Alfred's response
        await track_convo('assistant', response_text)

        # Reply to the message
        await message.reply(response_text)

        logger.info(f"Handled reply: {response_text}")
    else:
        # This message is not a reply; handle accordingly
        pass

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
        # 'weather': 'Get current weather information.',
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

    if message.content.startswith('?'):
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
