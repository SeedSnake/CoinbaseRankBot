from discord.ext import commands
import discord
import json
import os
from datetime import datetime

# Import your necessary modules here
from api.apps import current_rank_coinbase, current_rank_wallet, current_rank_binance, current_rank_cryptodotcom, get_bitcoin_price_usd
from utilities import number_to_emoji, evaluate_sentiment, weighted_average_sentiment_calculation
from data_management.database import AppRankTracker
from tracker import RankTracker

# Create tracker instances
coinbase_tracker = AppRankTracker('Coinbase', 'data/rank_data_coinbase.json')
wallet_tracker = AppRankTracker('Wallet', 'data/rank_data_wallet.json')
binance_tracker = AppRankTracker('Binance', 'data/rank_data_binance.json')
cryptodotcom_tracker = AppRankTracker('Crypto.com', 'data/rank_data_cryptodotcom.json')

# Setup a bot instance here if not passed from bot.py
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize sentiment calculation
average_sentiment_calculation = weighted_average_sentiment_calculation()

async def send_error_message_set_alert(ctx, additional_info=""):
    embed = discord.Embed(
        title="❌ Missing argument",
        description="One or more arguments are missing.",
        color=discord.Color.red()
    )
    embed.add_field(name="Format Correct", value="``!alert`` ``<app-name>`` ``<operator>`` ``<rank>``")
    if additional_info:
        embed.add_field(name="Error", value=additional_info)
    embed.add_field(name="Example", value="``!alert coinbase > 10``")
    avatar_url = ctx.author.avatar.url if ctx.author.avatar else None
    embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=avatar_url if avatar_url else discord.Embed.Empty)
    await ctx.send(embed=embed)

async def send_error_message_remove_alert(ctx, additional_info=""):
    embed = discord.Embed(
        title="❌ Missing argument",
        description="One or more arguments are missing.",
        color=discord.Color.red()
    )
    embed.add_field(name="Format Correct", value="``!remove_alert`` ``<app-name>``")
    if additional_info:
        embed.add_field(name="Error", value=additional_info)
    embed.add_field(name="Example", value="``!remove_alert coinbase``")
    avatar_url = ctx.author.avatar.url if ctx.author.avatar else None
    embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=avatar_url if avatar_url else discord.Embed.Empty)
    await ctx.send(embed=embed)

@bot.command()
async def coinbase(ctx):
    rank_number_coinbase = current_rank_coinbase()
    now = datetime.now()
    current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

    # Assume wallet_tracker is also defined
    sentiment_text, sentiment_image_filename = evaluate_sentiment()
    change_symbol = coinbase_tracker.compare_ranks(rank_number_coinbase)
    highest_rank, lowest_rank = coinbase_tracker.get_extreme_ranks()

    embed = discord.Embed(title="Coinbase Statistics", description="Real-time tracking and analysis of the Coinbase app ranking.", color=0x00ff00)

    # Attach the main thumbnail
    file_thumb = discord.File("assets\coinbase-coin-seeklogo.png", filename="coinbase_logo.png")
    embed.set_thumbnail(url="attachment://coinbase_logo.png")

    # Add fields before Market Sentiment
    embed.add_field(name="🏆 Current Rank", value=f"``#️⃣{number_to_emoji(rank_number_coinbase)} in Finance on {current_datetime_hour}``", inline=False)
    embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)
    if highest_rank:
        embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"``#️⃣{number_to_emoji(highest_rank['rank'])} on {highest_rank['timestamp']}``", inline=True)
    if lowest_rank:
        embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"``#️⃣{number_to_emoji(lowest_rank['rank'])} on {lowest_rank['timestamp']}``", inline=True)

    # Market Sentiment field and image below it
    embed.add_field(name="🚥 Market Sentiment", value=f"Score: ``{average_sentiment_calculation}``\nFeeling: ``{sentiment_text}``\n", inline=False)

    # Attach the sentiment image
    file_sentiment = discord.File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
    embed.set_image(url=f"attachment://{sentiment_image_filename}")

    # Footer and sending the message
    avatar_url = ctx.author.avatar.url if ctx.author.avatar else None
    embed.set_footer(text=f"Requested by {ctx.author.display_name}, {current_datetime_hour}.", icon_url=avatar_url if avatar_url else discord.Embed.Empty)

    coinbase_tracker.save_rank(rank_number_coinbase)

    await ctx.send(files=[file_thumb, file_sentiment], embed=embed)

@bot.command()
async def cwallet(ctx):
    rank_number_wallet = current_rank_wallet()  # Ensure you have a function that fetches the current rank for Wallet
    now = datetime.now()
    current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

    # Assume wallet_tracker is also defined
    sentiment_text, sentiment_image_filename = evaluate_sentiment()
    change_symbol = wallet_tracker.compare_ranks(rank_number_wallet)
    highest_rank, lowest_rank = wallet_tracker.get_extreme_ranks()

    embed = discord.Embed(title="Coinbase's Wallet Statistics", description="Real-time tracking and analysis of the Coinbase's Wallet app ranking.", color=0x00ff00)

    # Attach the main thumbnail
    file_thumb = discord.File("assets\coinbase-wallet-seeklogo.png", filename="coinbase_wallet_logo.png")
    embed.set_thumbnail(url="attachment://coinbase_wallet_logo.png")

    # Add fields before Market Sentiment
    embed.add_field(name="🏆 Current Rank", value=f"``#️⃣{number_to_emoji(rank_number_wallet)} in Finance on {current_datetime_hour}``", inline=False)
    embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)
    if highest_rank:
        embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"``#️⃣{number_to_emoji(highest_rank['rank'])} on {highest_rank['timestamp']}``", inline=True)
    if lowest_rank:
        embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"``#️⃣{number_to_emoji(lowest_rank['rank'])} on {lowest_rank['timestamp']}``", inline=True)

    # Market Sentiment field and image below it
    embed.add_field(name="🚥 Market Sentiment", value=f"Score: ``{average_sentiment_calculation}``\nFeeling: ``{sentiment_text}``\n", inline=False)

    # Attach the sentiment image
    file_sentiment = discord.File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
    embed.set_image(url=f"attachment://{sentiment_image_filename}")

    # Footer and sending the message
    avatar_url = ctx.author.avatar.url if ctx.author.avatar else None
    embed.set_footer(text=f"Requested by {ctx.author.display_name}, {current_datetime_hour}.", icon_url=avatar_url if avatar_url else discord.Embed.Empty)

    wallet_tracker.save_rank(rank_number_wallet)

    await ctx.send(files=[file_thumb, file_sentiment], embed=embed)

@bot.command()
async def binance(ctx):
    rank_number_binance = current_rank_binance()
    now = datetime.now()
    current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

    # Assume binance_tracker is also defined
    sentiment_text, sentiment_image_filename = evaluate_sentiment()
    change_symbol = binance_tracker.compare_ranks(rank_number_binance)
    highest_rank, lowest_rank = binance_tracker.get_extreme_ranks()

    embed = discord.Embed(title="Binance Statistics", description="Real-time tracking and analysis of the Binance app ranking.", color=0x00ff00)

    # Attach the main thumbnail
    file_thumb = discord.File("assets/binance-smart-chain-bsc-seeklogo.png", filename="binance_logo.png")
    embed.set_thumbnail(url="attachment://binance_logo.png")

    # Add fields before Market Sentiment
    embed.add_field(name="🏆 Current Rank", value=f"``#️⃣{number_to_emoji(rank_number_binance)} in Finance on {current_datetime_hour}``", inline=False)
    embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)
    if highest_rank:
        embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"``#️⃣{number_to_emoji(highest_rank['rank'])} on {highest_rank['timestamp']}``", inline=True)
    if lowest_rank:
        embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"``#️⃣{number_to_emoji(lowest_rank['rank'])} on {lowest_rank['timestamp']}``", inline=True)

    # Market Sentiment field and image below it
    embed.add_field(name="🚥 Market Sentiment", value=f"Score: ``{average_sentiment_calculation}``\nFeeling: ``{sentiment_text}``\n", inline=False)

    # Attach the sentiment image
    file_sentiment = discord.File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
    embed.set_image(url=f"attachment://{sentiment_image_filename}")

    # Footer and sending the message
    avatar_url = ctx.author.avatar.url if ctx.author.avatar else None
    embed.set_footer(text=f"Requested by {ctx.author.display_name}, {current_datetime_hour}.", icon_url=avatar_url if avatar_url else discord.Embed.Empty)

    binance_tracker.save_rank(rank_number_binance)

    await ctx.send(files=[file_thumb, file_sentiment], embed=embed)

@bot.command()
async def cryptocom(ctx):
    rank_number_cryptodotcom = current_rank_cryptodotcom()
    now = datetime.now()
    current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

    # Assume cryptodotcom_tracker is also defined
    sentiment_text, sentiment_image_filename = evaluate_sentiment()
    change_symbol = cryptodotcom_tracker.compare_ranks(rank_number_cryptodotcom)
    highest_rank, lowest_rank = cryptodotcom_tracker.get_extreme_ranks()

    embed = discord.Embed(title="Crypto.com Statistics", description="Real-time tracking and analysis of the Crypto.com app ranking.", color=0x00ff00)

    # Attach the main thumbnail
    file_thumb = discord.File("assets/crypto-com-seeklogo.png", filename="cryptodotcom_logo.png")
    embed.set_thumbnail(url="attachment://cryptodotcom_logo.png")

    # Add fields before Market Sentiment
    embed.add_field(name="🏆 Current Rank", value=f"``#️⃣{number_to_emoji(rank_number_cryptodotcom)} in Finance on {current_datetime_hour}``", inline=False)
    embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)
    if highest_rank:
        embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"``#️⃣{number_to_emoji(highest_rank['rank'])} on {highest_rank['timestamp']}``", inline=True)
    if lowest_rank:
        embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"``#️⃣{number_to_emoji(lowest_rank['rank'])} on {lowest_rank['timestamp']}``", inline=True)

    # Market Sentiment field and image below it
    embed.add_field(name="🚥 Market Sentiment", value=f"Score: ``{average_sentiment_calculation}``\nFeeling: ``{sentiment_text}``\n", inline=False)

    # Attach the sentiment image
    file_sentiment = discord.File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
    embed.set_image(url=f"attachment://{sentiment_image_filename}")

    # Footer and sending the message
    avatar_url = ctx.author.avatar.url if ctx.author.avatar else None
    embed.set_footer(text=f"Requested by {ctx.author.display_name}, {current_datetime_hour}.", icon_url=avatar_url if avatar_url else discord.Embed.Empty)

    cryptodotcom_tracker.save_rank(rank_number_cryptodotcom)

    await ctx.send(files=[file_thumb, file_sentiment], embed=embed)

@bot.command()
async def alert(ctx, app_name: str = None, operator: str = None, rank: int = None):
    # Verify if all args are valid
    if app_name is None or operator is None or rank is None:
        await send_error_message_set_alert(ctx)
        return
    
    if operator not in ['>', '<', '>=', '<=']:
        await ctx.send("Invalid operator. Please use one of the following: '>', '<', '>=', '<='.")
        return
    
    alert_data = {
        'user_id': ctx.author.id,
        'app_name': app_name.lower(),
        'operator': operator,
        'rank': rank
    }

    os.makedirs('data', exist_ok=True)

    try:
        alerts = []
        # Check if file exists and read existing data
        if os.path.exists('data/alerts.json'):
            with open('data/alerts.json', 'r') as f:
                alerts = json.load(f)
        
        # Check for duplicate alerts
        for existing_alert in alerts:
            if (existing_alert['user_id'] == ctx.author.id and
                existing_alert['app_name'] == app_name.lower() and
                existing_alert['operator'] == operator and
                existing_alert['rank'] == rank):
                embed = discord.Embed(description=f"❌ Alert for ``{app_name}`` when rank ``{operator} {rank}`` already exists.", color=0xff0000)
                avatar_url = ctx.author.avatar.url if ctx.author.avatar else None
                embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=avatar_url if avatar_url else discord.Embed.Empty)
                await ctx.send(embed=embed)
                return
        
        # Add the new alert if no duplicates
        alerts.append(alert_data)
        with open('data/alerts.json', 'w') as f:
            json.dump(alerts, f, indent=4)

        embed = discord.Embed(description=f"✅🔔 Alert set for {app_name} when rank ``{operator} {rank}``.", color=0x00ff00)
        avatar_url = ctx.author.avatar.url if ctx.author.avatar else None
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=avatar_url if avatar_url else discord.Embed.Empty)
        await ctx.send(embed=embed)

    except Exception as e:
        print(f"Failed to set or check alerts due to an error: {e}")
        await ctx.send("🚨 Failed to set alert due to an internal error.")

@bot.command(name='rmalert')
async def rmalert(ctx, app_name: str = None):
    if app_name is None:
        embed = discord.Embed(description="❌ Please specify an app name to remove its alert.", color=discord.Color.red())
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else discord.Embed.Empty)
        await ctx.send(embed=embed)
        return

    user_id = ctx.author.id
    alert_file_path = 'data/alerts.json'  # Ensure this path is correct in your file structure

    try:
        with open(alert_file_path, 'r+') as file:
            alerts = json.load(file)
            new_alerts = [alert for alert in alerts if not (alert['user_id'] == user_id and alert['app_name'].lower() == app_name.lower())]

            if len(alerts) == len(new_alerts):
                embed = discord.Embed(description=f"🙅‍♂️ No alert found for ``{app_name.capitalize()}`` that belongs to you.", color=discord.Color.red())
            else:
                file.seek(0)
                json.dump(new_alerts, file, indent=4)
                file.truncate()
                embed = discord.Embed(description=f"🚮 Alert for ``{app_name.capitalize()}`` has been successfully removed.", color=discord.Color.green())

            embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else discord.Embed.Empty)
            await ctx.send(embed=embed)

    except FileNotFoundError:
        embed = discord.Embed(description="🚨 Alert data file not found.", color=discord.Color.red())
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else discord.Embed.Empty)
        await ctx.send(embed=embed)
    except json.JSONDecodeError:
        embed = discord.Embed(description="🚨 Error reading the alert data.", color=discord.Color.red())
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else discord.Embed.Empty)
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(description="🚨 Failed to remove the alert due to an error.", color=discord.Color.red())
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else discord.Embed.Empty)
        await ctx.send(embed=embed)
        print(f"Error when trying to remove alert: {e}")

@bot.command(name='myalerts')
async def myalerts(ctx):
    user_id = ctx.author.id
    alert_file_path = 'data/alerts.json'  # Adjust path as necessary

    try:
        with open(alert_file_path, 'r') as file:
            alerts = json.load(file)
            user_alerts = [alert for alert in alerts if alert['user_id'] == user_id]

        if not user_alerts:
            embed = discord.Embed(description="🤷‍♂️ You have no active alerts.", color=discord.Color.blue())
        else:
            embed = discord.Embed(title="🔂🔔 Your Active Alerts", description="", color=discord.Color.green())
            for alert in user_alerts:
                embed.add_field(name=f"``✅ {alert['app_name'].title()} Alert``",
                                value=f"``Trigger: {alert['operator']} {alert['rank']}``",
                                inline=False)

        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else discord.Embed.Empty)
        await ctx.send(embed=embed)

    except FileNotFoundError:
        embed = discord.Embed(description="🚨 Alert data file not found.", color=discord.Color.red())
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else discord.Embed.Empty)
        await ctx.send(embed=embed)
    except json.JSONDecodeError:
        embed = discord.Embed(description="🚨 Error reading the alert data.", color=discord.Color.red())
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else discord.Embed.Empty)
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(description="🚨 An error occurred while retrieving your alerts.", color=discord.Color.red())
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else discord.Embed.Empty)
        await ctx.send(embed=embed)
        print(f"Error retrieving alerts: {e}")

@bot.command(name='rmall')
async def rmall(ctx):
    user_id = ctx.author.id
    try:
        # Load the current alerts from the file
        if os.path.exists('data/alerts.json'):
            with open('data/alerts.json', 'r') as file:
                alerts = json.load(file)
            
            # Filter out alerts for the user
            alerts = [alert for alert in alerts if alert['user_id'] != user_id]

            # Write the updated alerts back to the file
            with open('data/alerts.json', 'w') as file:
                json.dump(alerts, file, indent=4)
            
            embed = discord.Embed(title="🚮✅ Alerts Removed", description="All your alerts have been successfully removed.", color=0x00ff00)
            embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
            await ctx.send(embed=embed)
        else:
            await ctx.send("🤷‍♂️ No alert file found or no alerts set.")

    except Exception as e:
        await ctx.send("🚨 Failed to remove alerts due to an error.")
        print(f"Error when trying to remove all alerts: {e}")

@bot.command(name='ranks')
async def ranks(ctx):
    rank_tracker = RankTracker(ctx.bot)  # Assuming you create a new instance or pass an existing one
    bitcoin_price = get_bitcoin_price_usd()  # Get the current price of Bitcoin
    bitcoin_emoji_id = "1234500592559194164"  # Replace with the actual ID of your Bitcoin emoji
    bitcoin_emoji = f"<:bitcoin:{bitcoin_emoji_id}>"
    bitcoin_price_text = f"``Current Bitcoin Price: 💲{bitcoin_price:,.2f} USD``" if bitcoin_price != "Unavailable" else f"{bitcoin_emoji} Bitcoin Price: Unavailable"

    embed = discord.Embed(title="Crypto App Ranks", description="Current and historical ranks of major crypto apps.", color=0x00ff00)
    embed.add_field(name=f"{bitcoin_emoji} Bitcoin Price", value=bitcoin_price_text, inline=False)  # Add Bitcoin price at the top
    apps = ["coinbase", "wallet", "binance", "cryptocom"]
    emoji_ids = {
        "coinbase": "<:coinbase_icon:1234492789967032330>",  # Replace with actual emoji ID
        "wallet": "<:wallet_icon:1234492792320036925>",
        "binance": "<:binance_icon:1234492788616331295>",
        "cryptocom": "<:cryptocom_icon:1234492791355080874>"
    }

    # Fetch all ranks once to reduce repetitive calls
    current_ranks = rank_tracker.fetch_all_ranks()

    for idx, app in enumerate(apps):
        current_rank = current_ranks[idx]
        yesterday_rank = rank_tracker.get_historical_rank(app, days_back=1)
        last_week_rank = rank_tracker.get_historical_rank(app, days_back=7)
        last_month_rank = rank_tracker.get_historical_rank(app, months_back=1)

        # Calculate the difference and set the appropriate arrow
        if current_rank is not None and yesterday_rank is not None:
            if current_rank < yesterday_rank:
                change_icon = "🔼+"  # Arrow up
                change = yesterday_rank - current_rank
            elif current_rank > yesterday_rank:
                change_icon = "🔻-"  # Arrow down
                change = current_rank - yesterday_rank
            else:
                change_icon = ""  # No change
                change = ""
            change_text = f"{change_icon}{change}" if change_icon else "No change"
        else:
            change_text = "Data unavailable"

        embed.add_field(
            name=f"{emoji_ids[app]} {app.capitalize()} Rank",
            value=f"``Current: #️⃣{number_to_emoji(current_rank)} ({change_text}) | Yesterday: #️⃣{number_to_emoji(yesterday_rank)} | Last Week: #️⃣{number_to_emoji(last_week_rank)} | Last Month: #️⃣{number_to_emoji(last_month_rank)}``",
            inline=False
        )

    await ctx.send(embed=embed)

def setup_commands(bot):
    bot.add_command(coinbase)
    bot.add_command(binance)
    bot.add_command(cryptocom)
    bot.add_command(cwallet)
    bot.add_command(alert)
    bot.add_command(rmalert)
    bot.add_command(myalerts)
    bot.add_command(rmall)
    bot.add_command(ranks)