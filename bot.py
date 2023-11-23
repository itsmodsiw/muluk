import discord
import os
import requests


def load_whitelist() :
    # URL to your whitelist file in the GitHub repository
    url = 'https://raw.githubusercontent.com/modsiw/muluk/main/whitelist.txt'
    response = requests.get(url)
    return response.text.splitlines()


def extract_links(message) :
    # Implement your logic here to extract links from the message
    # For simplicity, let's assume each word is checked if it's a URL
    words = message.split()
    return [word for word in words if word.startswith("http")]


client = discord.Client()


@client.event
async def on_ready() :
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message) :
    if message.author == client.user :
        return

    whitelist = load_whitelist()
    message_links = extract_links(message.content)

    for link in message_links :
        if not any(whitelisted_domain in link for whitelisted_domain in whitelist) :
            await message.delete()
            break  # Optionally, you can send a warning message or log this action


# Fetching the bot token from Heroku's config vars
client.run(os.getenv('DISCORD_BOT_TOKEN'))
