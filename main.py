# Existing Imports
import json
import os

import discord
import dotenv

from alfred import AlfredChat
from api.coin import CoinInfo
from log import setup_logger  # Assuming this is the file where your logging setup resides

# Initialize Global Variable
alfred_instances = []


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
ongoing_conversations = {}

@client.event
async def on_message(message):
    global users
    for i in range(0, 1):
        logger.info(f"Received message from {message.author.name}: {message.content}")

    # Ignore self
    if message.author == client.user:
        return

    # Owner-specific command
    # if message.author.name == owner and message.content == 'hello':
    #     await message.channel.send('All hail to the chief')

    # Make user profile
    user_id = str(message.author.id)
    if user_id not in users:
        logger.info(f"Creating new profile for {message.author.name}")
        users[user_id] = {'username': message.author.name, 'rep': 0, 'total_prompts': 0}
        await save_users()

    # Alfred Chat
    if message.content.startswith('!'):
        for i in range(0, 1):
            # reset on fresh prompt
            ongoing_conversations.clear()
            prompt = message.content[1:]
            ongoing_conversations[user_id] = message.author.name
            users[user_id]['total_prompts'] += 1
            await save_users()

            # Create AlfredChat object
            alfred = AlfredChat()

            res = alfred.return_completion(prompt=prompt)
            reply = await message.reply(res)
            ongoing_conversations[reply.id] = {'user-msg-1': prompt, 'alfred-msg-1': res, 'reply_count': 1}
            logger.info(f"Sent reply: {res}")
            i += 1

    elif message.reference:  # Check if the message is a reply

        if message.reference.message_id in ongoing_conversations:

            original_context = ongoing_conversations[message.reference.message_id]

            original_context['reply_count'] += 1

            # Add new messages to context

            original_context[f'user-msg-{original_context["reply_count"]}'] = message.content


            # Create a simplified string from the original context to pass as the prompt

            simple_context = ""

            for i in range(1, original_context["reply_count"] + 1):
                simple_context += f'User: {original_context.get(f"user-msg-{i}", "")}\n'

                simple_context += f'Alfred: {original_context.get(f"alfred-msg-{i}", "")}\n'

            # Get Alfred's new reply based on the new context

            new_res = AlfredChat().return_completion(prompt=simple_context)

            reply = await message.reply(new_res)

            # Update the ongoing conversations with Alfred's new message

            original_context[f'alfred-msg-{original_context["reply_count"]}'] = new_res

            ongoing_conversations[reply.id] = original_context
    # TODO add additional features
    elif message.content.startswith('&'):
        if message.content[:5] == '&coin':
            await message.channel.send('coin price requested')
            symbol = message.content[6:].strip()  # Strip removes leading and trailing whitespace
            logger.info(f"Coin price requested for {symbol if symbol else 'bitcoin'}")
            coin = CoinInfo(symbol if symbol else 'bitcoin')  # Default to 'bitcoin' if no symbol provided
            await message.channel.send(coin.get_price())
            # await message.channel.send(coin.get_change())

    elif message.content[:5] == '&help':
        #     tell user about your various fucntions
        #  also log which user sent the message, and at what time in what channel
        await message.channel.send('help requested')
        logger.info(f"Help requested by {message.author.name}")



    elif message.content == '&':
        logger.info("Received standalone '&', no action taken.")
        await message.channel.send("Received standalone '&', no action taken.")
    else:
        logger.info("Unknown command starting with '&' received.")
        # await message.channel.send("Unknown command starting with '&' received.")

        # elif message.content[:4] == '&run':
        #     logger.info('code run feature requested')
        #
        #
        #     if message.attachments:
        #         file_url = message.attachments[0].url
        #         # You can now use the file URL for further processing
        #
        #         await message.channel.send(f"File uploaded, URL: {file_url}")


client.run(DISCORD_APP_TOKEN)
