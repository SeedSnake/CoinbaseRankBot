from discord.ext import commands
from discord import Intents, app_commands
import discord
import asyncio
import os

from config import BOT_TOKEN
from tracker import RankTracker
from commands import setup_commands  # Ensure this imports your command setup functions properly

class MyBot(commands.Bot):
    def __init__(self):
        intents = Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.guilds = True
        super().__init__(command_prefix='!', intents=intents, application_id=os.getenv('DISCORD_APPLICATION_ID'))

    async def setup_hook(self):
        await self.tree.sync()

    async def start_tracker():
        asyncio.new_event_loop().run_until_complete(tracker.run())

    async def on_ready(self):
        print(f'Logged in as {self.user.name}')
        bot.loop.create_task(tracker.run())
        await self.tree.sync()  # Ensure commands are synced globally

    async def on_disconnect(self):
        print("Bot is disconnecting...")
        asyncio.run_coroutine_threadsafe(tracker.shutdown(), bot.loop)

    async def on_guild_join(self, guild):
        # Automatically add custom emojis to guilds when the bot joins
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

bot = MyBot()
tracker = RankTracker(bot)

async def main():
    await setup_commands(bot)
    await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())