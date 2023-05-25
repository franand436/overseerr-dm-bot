import discord
from discord.ext import commands
import aiohttp

BOT_TOKEN = 'PLACE BOT TOKEN HERE'
CHANNEL_ID = 'PLACE_CHANNEL_ID_HERE_MINUS_QUOTES'

bot = commands.Bot(command_prefix='!', intents = discord.Intents.all())

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print("Hello World! overseerr-dm-bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello World! overseerr-dm-bot is ready!") #Sends message in channel as a sign that its ready to go.
#Profile picture for the bot
    await set_avatar(BOT_TOKEN, 'https://seedit4.me/assets/img/icons/software/overseerr.png')

async def set_avatar(bot_token, avatar_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(avatar_url) as response:
            avatar_data = await response.read()

    await bot.user.edit(avatar=avatar_data)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # List of target user IDs
    target_user_ids = [
        00000000000000000, #User 1 Discord ID
        11111111111111111, #User 2 Discord ID (repeat for however man users you have.)
        ]

    mentioned_users = [
        user for user in message.mentions if user.id in target_user_ids
    ]

    for user in mentioned_users:
        target_user = await bot.fetch_user(user.id)

        # Remove the mention and username from the message content
        content_without_mention = message.clean_content.replace(user.mention, "").replace(f"@{user.name}", "").strip()

        dm_content = f'{content_without_mention}'

        # Include embedded content, if available
        if len(message.embeds) > 0:
            for embed in message.embeds:
                # Add embedded title and description
                if embed.title:
                    dm_content += f'\nYour Plex request is now available 😊\n**{embed.title}**' #Uses dicrod rich text to bolld the title. Format intro text to your liking.

        await target_user.send(dm_content)

    await bot.process_commands(message)

# Run the bot
bot.run(BOT_TOKEN)
