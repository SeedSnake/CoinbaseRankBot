import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import asyncio
from discord.ext import commands
from utilities import evaluate_sentiment, weighted_average_sentiment_calculation
from data_management.database import AppRankTracker
import discord
import json
import os
import logging
import aiohttp
import aiofiles

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RankTracker:
    def __init__(self, bot):
        self.bot = bot
        self.url_coinbase = "https://apps.apple.com/us/app/coinbase-buy-sell-bitcoin/id886427730"
        self.url_coinbase_wallet = "https://apps.apple.com/us/app/coinbase-wallet-nfts-crypto/id1278383455"
        self.url_binance = "https://apps.apple.com/us/app/binance-us-buy-bitcoin-eth/id1492670702"
        self.url_cryptodotcom = "https://apps.apple.com/us/app/crypto-com-buy-bitcoin-sol/id1262148500"

    async def fetch_rank(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        text = await response.text()
                        soup = BeautifulSoup(text, 'html.parser')
                        rank_element = soup.find('a', class_='inline-list__item', href=True, text=lambda t: 'in Finance' in t)
                        if rank_element:
                            rank_text = rank_element.get_text(strip=True)
                            rank_number = int(''.join(filter(str.isdigit, rank_text)))
                            return rank_number
                        else:
                            print("Rank element not found.")
                            return None
                    else:
                        print(f"HTTP Error {response.status} for URL: {url}")
                        return None
        except Exception as e:
            print(f"Error fetching rank: {e}")
            return None

    async def fetch_coinbase_rank(self):
        return await self.fetch_rank(self.url_coinbase)

    async def fetch_coinbase_wallet_rank(self):
        return await self.fetch_rank(self.url_coinbase_wallet)
    
    async def fetch_binance_rank(self):
        return await self.fetch_rank(self.url_binance)
    
    async def fetch_cryptodotcom_rank(self):
        return await self.fetch_rank(self.url_cryptodotcom)
    
    async def fetch_all_ranks(self):
        # Gather all ranks concurrently
        coinbase_rank, wallet_rank, binance_rank, cryptocom_rank = await asyncio.gather(
            self.fetch_coinbase_rank(),
            self.fetch_coinbase_wallet_rank(),
            self.fetch_binance_rank(),
            self.fetch_cryptodotcom_rank()
        )
        return coinbase_rank, wallet_rank, binance_rank, cryptocom_rank
    
    async def save_rank_to_history(self, app_name, rank):
        now = datetime.now(timezone.utc)
        data_path = 'data/app_ranks.json'
        try:
            # Async file operations
            if os.path.exists(data_path):
                async with aiofiles.open(data_path, 'r') as file:
                    data = await file.read()
                    data = json.loads(data) if data else {}
            else:
                data = {}

            data[app_name] = {
                'rank': rank,
                'timestamp': now.isoformat()
            }

            async with aiofiles.open(data_path, 'w') as file:
                await file.write(json.dumps(data, indent=4))
        except Exception as e:
            print(f"Error while saving rank data: {e}")

    async def get_historical_rank(self, app_name, days_back=None, months_back=None):
        file_path = f'data/{app_name}_rank_history.json'
        if not os.path.exists(file_path):
            return "No data file found"

        today = datetime.now()
        if days_back:
            target_date = today - timedelta(days=days_back)
        elif months_back:
            target_date = today - timedelta(days=30 * months_back)  # approximate month adjustment
        else:
            return "Invalid or missing time parameter"
        
        year, month, day = target_date.strftime('%Y'), target_date.strftime('%m'), target_date.strftime('%d')

        try:
            async with aiofiles.open(file_path, 'r') as file:
                data = await file.read()
                data = json.loads(data)
            # Fetch the last recorded rank for the target day
            day_data = data.get(year, {}).get(month, {}).get(day, [])
            if day_data:
                return day_data[-1]['rank']  # return the last rank of the day
            else:
                return "No rank data available"
        except Exception as e:
            print(f"Error accessing file {file_path}: {e}")
            return "Error processing the historical data"

    async def track_rank(self):
        logging.info("Starting to track rank.")

        try:
            coinbase_rank = await self.fetch_coinbase_rank()
            if coinbase_rank is not None:
                logging.info(f"Fetched Coinbase rank: {coinbase_rank}")
                await self.save_rank_to_history('coinbase', coinbase_rank)
            else:
                logging.warning("Failed to fetch Coinbase rank.")
        except Exception as e:
            logging.error(f"Error while fetching/saving Coinbase rank: {e}")

        try:
            coinbase_wallet_rank = await self.fetch_coinbase_wallet_rank()
            if coinbase_wallet_rank is not None:
                logging.info(f"Fetched Coinbase Wallet rank: {coinbase_wallet_rank}")
                await self.save_rank_to_history("wallet", coinbase_wallet_rank)
            else:
                logging.warning("Failed to fetch Coinbase Wallet rank.")
        except Exception as e:
            logging.error(f"Error while fetching/saving Coinbase Wallet rank: {e}")

        try:
            binance_rank = await self.fetch_binance_rank()
            if binance_rank is not None:
                logging.info(f"Fetched Binance rank: {binance_rank}")
                await self.save_rank_to_history("binance", binance_rank)
            else:
                logging.warning("Failed to fetch Binance rank.")
        except Exception as e:
            logging.error(f"Error while fetching/saving Binance rank: {e}")

        try:
            cryptodotcom_rank = await self.fetch_cryptodotcom_rank()
            if cryptodotcom_rank is not None:
                logging.info(f"Fetched Crypto.com rank: {cryptodotcom_rank}")
                await self.save_rank_to_history("cryptodotcom", cryptodotcom_rank)
            else:
                logging.warning("Failed to fetch Crypto.com rank.")
        except Exception as e:
            logging.error(f"Error while fetching/saving Crypto.com rank: {e}")

        logging.info("Finished tracking rank.")

    async def get_current_rank(self, app_name):
        file_path = 'data/app_ranks.json'
        try:
            # Asynchronously open and read the file
            async with aiofiles.open(file_path, 'r') as file:
                data = await file.read()
                data = json.loads(data)
                if app_name in data:
                    return data[app_name]['rank']
        except IOError as e:
            print(f"Error accessing file {file_path}: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return None

    def evaluate_condition(self, current_rank, operator, rank):
        if operator == '>':
            return current_rank > rank
        elif operator == '<':
            return current_rank < rank
        elif operator == '>=':
            return current_rank >= rank
        elif operator == '<=':
            return current_rank <= rank
        elif operator == '==':
            return current_rank == rank
        else:
            logging.error(f"Unsupported operator {operator}")
            return False

    async def check_alerts(self):
        logging.info("Starting to check alerts.")
        while True:
            try:
                # Always re-read the alert conditions on each loop iteration
                async with aiofiles.open('data/alerts.json', 'r') as f:
                    data = await f.read()
                    alerts = json.loads(data) if data else []

                current_ranks = {
                    'coinbase': await self.get_current_rank('coinbase'),
                    'cwallet': await self.get_current_rank('wallet'),
                    'binance': await self.get_current_rank('binance'),
                    'cryptocom': await self.get_current_rank('cryptodotcom')
                }

                for alert in alerts:
                    user_id = alert['user_id']
                    app = alert['app_name']
                    current_rank = current_ranks.get(app, None)
                    if current_rank and self.evaluate_condition(current_rank, alert['operator'], alert['rank']):
                        await self.send_alert(user_id, app, current_rank)

                logging.info("Alert checking completed.")
            except Exception as e:
                logging.error(f"Failed to check alerts: {e}")

            await asyncio.sleep(10)  # Adjust timing as necessary

    async def send_alert(self, user_id, app_name, rank):
        logging.info(f"Preparing to send alert for {app_name} to user {user_id}")

        sentiment_text, sentiment_image_filename = await evaluate_sentiment()
        average_sentiment_calculation = await weighted_average_sentiment_calculation()

        try:
            user = await self.bot.fetch_user(user_id)
            if user:
                embed = discord.Embed(title=f"📢🔔 Alert for {app_name.capitalize()}!",
                                      description=f"The rank condition for **``{app_name.capitalize()}``** has been met! Current rank is **``{rank}``**.",
                                      color=0x00ff00)
                
                embed.add_field(name="Current Market Sentiment:", value=f"Score: ``{average_sentiment_calculation}``\nFeeling: ``{sentiment_text}``\n", inline=False)
                
                # Ensure the sentiment image file exists before attempting to send it
                if os.path.exists(f"assets/{sentiment_image_filename}"):
                    file_sentiment = discord.File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
                    embed.set_image(url=f"attachment://{sentiment_image_filename}")
                else:
                    logging.warning(f"Sentiment image file not found: {sentiment_image_filename}")

                embed.set_footer(text=f"Alert requested by {user.display_name}", icon_url=user.avatar.url if user.avatar else discord.Embed.Empty)

                await user.send(files=[file_sentiment] if 'file_sentiment' in locals() else [], embed=embed)
                logging.info(f"Alert sent to {user.display_name}")
            else:
                logging.warning(f"User {user_id} not found.")
        except discord.HTTPException as e:
            logging.error(f"Failed to send message to {user_id}: {e}")
        except Exception as e:
            logging.error(f"An error occurred while sending an alert to {user_id}: {e}")

    async def update_bot_status(self):
        logging.info("Starting to update bot status.")

        app_urls = [
            ("coinbase", self.url_coinbase),
            ("coinbase wallet", self.url_coinbase_wallet),
            ("binance", self.url_binance),
            ("crypto.com", self.url_cryptodotcom)
        ]
        status_index = 0
        while True:  # This loop will continuously update the status
            app_name, url = app_urls[status_index]
            try:
                rank = await self.fetch_rank(url)
                if rank is not None:
                    status_message = f"{app_name.capitalize()}: Rank #{rank}"
                    await self.bot.change_presence(activity=discord.Game(name=status_message))
                    logging.info(f"Status updated: {status_message}")
                else:
                    logging.warning(f"Failed to fetch rank for {app_name}")
            except Exception as e:
                logging.error(f"Error fetching rank for {app_name}: {e}")

            # Wait for some time before changing the status
            await asyncio.sleep(10)  # Change status every 10 seconds

            # Move to the next app status or loop back to the start
            status_index = (status_index + 1) % len(app_urls)

            logging.info("Bot status update loop completed one iteration.")

    async def run(self):
        while True:
            try:
                logging.info("Running tracker loop.")
                await asyncio.gather(
                    self.track_rank(),
                    self.check_alerts(),
                    self.update_bot_status()
                )
            except Exception as e:
                logging.error(f"An error occurred in the tracker loop: {e}")

            logging.info("Sleeping for 10 seconds.")
            await asyncio.sleep(10)  # Proper management of sleep to not block other operations

if __name__ == "__main__":
    bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
    tracker = RankTracker(bot)