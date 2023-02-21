import discord
import os
from alfred import AlfredChat
import logging

# discord stuff
intents = discord.Intents.default()
intents.message_content = True
DISCORD_APP_TOKEN = os.getenv("DISCORD_APP_TOKEN")
client = discord.Client(intents=intents)

# logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$'):
        # if a message starts with $, create a completion
        prompt = message.content[1:]
        res = AlfredChat(prompt=prompt).return_completion()
        await message.channel.send(res)




        # debugging
        # user = message.author
        # f = open('log.txt', 'a')
        # f.write(user + ': ' + prompt + '\n')
        # f.write("Alfred: " + res + '\n')
        # print(user + ': ' + prompt + '\n')
        # print("Alfred: " + res + '\n')

        # print(message.author)


# print(handler)
client.run(DISCORD_APP_TOKEN, log_handler=handler)