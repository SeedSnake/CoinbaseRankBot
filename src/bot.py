from discord.ext import commands
from discord import Intents
import discord
import asyncio
import os

from config import BOT_TOKEN
from tracker import RankTracker
from commands import setup_commands  # Ensure this properly imports your command setup functions

class MyBot(commands.Bot):
    def __init__(self):
        intents = Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.guilds = True
        super().__init__(command_prefix='!', intents=intents, application_id=os.getenv('DISCORD_APPLICATION_ID'))

    async def setup_hook(self):
        self.tracker = RankTracker(self)  # Initialize tracker here
        self.loop.create_task(self.tracker.run())  # Start tracker as a background task
        await self.tree.sync()

    async def on_ready(self):
        print(f'Logged in as {self.user.name}')
        await self.tree.sync()  # Ensure commands are synced globally

    async def on_disconnect(self):
        print("Bot is disconnecting...")

    async def on_guild_join(self, guild):
        emoji_paths = {
            'coinbase': 'assets/coinbase_icon.png',
            'wallet': 'assets/wallet_icon.png',
            'binance': 'assets/binance_icon.png',
            'cryptocom': 'assets/cryptocom_icon.png'
        }
        for name, path in emoji_paths.items():
            with open(path, 'rb') as image_file:
                image = image_file.read()
            try:
                await guild.create_custom_emoji(name=name, image=image)
                print(f"Emoji {name} added to {guild.name}.")
            except discord.HTTPException as e:
                print(f"Failed to add emoji {name} to {guild.name}: {str(e)}")

async def main():
    bot = MyBot()
    await setup_commands(bot)
    await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())