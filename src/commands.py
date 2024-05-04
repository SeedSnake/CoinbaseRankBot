import discord
import json
import os
from datetime import datetime
from discord import app_commands, Interaction, File, Embed, Colour
from discord.ext import commands
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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

async def setup_commands(bot):

    async def send_error_message_set_alert(interaction: discord.Interaction, additional_info=""):
        embed = discord.Embed(
            title="❌ Missing argument",
            description="One or more arguments are missing.",
            color=discord.Color.red()
        )
        # Adjusted to remove the command prefix as slash commands don't use it
        embed.add_field(name="Format Correct", value="`/alert <app-name> <operator> <rank>`")
        if additional_info:
            embed.add_field(name="Error", value=additional_info)
        embed.add_field(name="Example", value="`/alert coinbase > 10`")
        avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
        embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=avatar_url if avatar_url else discord.Embed.Empty)
        # Use the response method appropriate for interactions
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def send_error_message_remove_alert(interaction: discord.Interaction, additional_info=""):
        embed = discord.Embed(
            title="❌ Missing argument",
            description="One or more arguments are missing.",
            color=discord.Color.red()
        )
        # Adjusted to remove the command prefix as slash commands don't use it
        embed.add_field(name="Format Correct", value="`/remove_alert <app-name>`")
        if additional_info:
            embed.add_field(name="Error", value=additional_info)
        embed.add_field(name="Example", value="`/remove_alert coinbase`")
        avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
        embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=avatar_url if avatar_url else discord.Embed.Empty)
        # Use the response method appropriate for interactions
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="coinbase", description="Get the current rank of the Coinbase app")
    async def coinbase_command(interaction: Interaction):
        
        average_sentiment_calculation = await weighted_average_sentiment_calculation()
        rank_number_coinbase = await current_rank_coinbase()
        now = datetime.now()
        current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

        sentiment_text, sentiment_image_filename = await evaluate_sentiment()
        change_symbol = await coinbase_tracker.compare_ranks(rank_number_coinbase)
        highest_rank, lowest_rank = await coinbase_tracker.get_extreme_ranks()

        embed = Embed(title="Coinbase Statistics", description="Real-time tracking and analysis of the Coinbase app ranking.", color=0x0052ff)
        file_thumb = File("assets/coinbase-coin-seeklogo.png", filename="coinbase_logo.png")
        embed.set_thumbnail(url="attachment://coinbase_logo.png")
        embed.add_field(name="🏆 Current Rank", value=f"#️⃣{number_to_emoji(rank_number_coinbase)} in Finance on {current_datetime_hour}", inline=False)
        embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)
        if highest_rank:
            embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"#️⃣{number_to_emoji(highest_rank['rank'])} on {highest_rank['timestamp']}", inline=True)
        if lowest_rank:
            embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"#️⃣{number_to_emoji(lowest_rank['rank'])} on {lowest_rank['timestamp']}", inline=True)
        embed.add_field(name="🚥 Market Sentiment", value=f"Score: {average_sentiment_calculation}\nFeeling: {sentiment_text}", inline=False)
        file_sentiment = File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
        embed.set_image(url=f"attachment://{sentiment_image_filename}")
        avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
        embed.set_footer(text=f"Requested by {interaction.user.display_name}, {current_datetime_hour}.", icon_url=avatar_url if avatar_url else None)

        await coinbase_tracker.save_rank(rank_number_coinbase)
        await interaction.response.send_message(files=[file_thumb, file_sentiment], embed=embed)

    @bot.tree.command(name="cwallet", description="Get the current rank of the Coinbase Wallet app")
    async def cwallet_command(interaction: Interaction):

        average_sentiment_calculation = await weighted_average_sentiment_calculation()
        rank_number_wallet = await current_rank_wallet()
        now = datetime.now()
        current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

        sentiment_text, sentiment_image_filename = await evaluate_sentiment()
        change_symbol = await wallet_tracker.compare_ranks(rank_number_wallet)
        highest_rank, lowest_rank = await wallet_tracker.get_extreme_ranks()

        embed = Embed(title="Coinbase's Wallet Statistics", description="Real-time tracking and analysis of the Coinbase's Wallet app ranking.", color=0x0052ff)
        file_thumb = File("assets/coinbase-wallet-seeklogo.png", filename="coinbase_wallet_logo.png")
        embed.set_thumbnail(url="attachment://coinbase_wallet_logo.png")

        embed.add_field(name="🏆 Current Rank", value=f"#️⃣{number_to_emoji(rank_number_wallet)} in Finance on {current_datetime_hour}", inline=False)
        embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)
        if highest_rank:
            embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"#️⃣{number_to_emoji(highest_rank['rank'])} on {highest_rank['timestamp']}", inline=True)
        if lowest_rank:
            embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"#️⃣{number_to_emoji(lowest_rank['rank'])} on {lowest_rank['timestamp']}", inline=True)

        embed.add_field(name="🚥 Market Sentiment", value=f"Score: {average_sentiment_calculation}\nFeeling: {sentiment_text}", inline=False)
        file_sentiment = File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
        embed.set_image(url=f"attachment://{sentiment_image_filename}")

        avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
        embed.set_footer(text=f"Requested by {interaction.user.display_name}, {current_datetime_hour}.", icon_url=avatar_url if avatar_url else None)

        await wallet_tracker.save_rank(rank_number_wallet)
        await interaction.response.send_message(files=[file_thumb, file_sentiment], embed=embed)

    @bot.tree.command(name="binance", description="Get the current rank of the Binance app")
    async def binance_command(interaction: Interaction):

        average_sentiment_calculation = await weighted_average_sentiment_calculation()
        rank_number_binance = await current_rank_binance()
        now = datetime.now()
        current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

        sentiment_text, sentiment_image_filename = await evaluate_sentiment()
        change_symbol = await binance_tracker.compare_ranks(rank_number_binance)
        highest_rank, lowest_rank = await binance_tracker.get_extreme_ranks()

        embed = Embed(title="Binance Statistics", description="Real-time tracking and analysis of the Binance app ranking.", color=0xf3ba2f)
        file_thumb = File("assets/binance-smart-chain-bsc-seeklogo.png", filename="binance_logo.png")
        embed.set_thumbnail(url="attachment://binance_logo.png")
        embed.add_field(name="🏆 Current Rank", value=f"#️⃣{number_to_emoji(rank_number_binance)} in Finance on {current_datetime_hour}", inline=False)
        embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)
        if highest_rank:
            embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"#️⃣{number_to_emoji(highest_rank['rank'])} on {highest_rank['timestamp']}", inline=True)
        if lowest_rank:
            embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"#️⃣{number_to_emoji(lowest_rank['rank'])} on {lowest_rank['timestamp']}", inline=True)
        embed.add_field(name="🚥 Market Sentiment", value=f"Score: {average_sentiment_calculation}\nFeeling: {sentiment_text}", inline=False)
        file_sentiment = File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
        embed.set_image(url=f"attachment://{sentiment_image_filename}")
        avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
        embed.set_footer(text=f"Requested by {interaction.user.display_name}, {current_datetime_hour}.", icon_url=avatar_url if avatar_url else None)

        await binance_tracker.save_rank(rank_number_binance)
        await interaction.response.send_message(files=[file_thumb, file_sentiment], embed=embed)

    @bot.tree.command(name="cryptocom", description="Get the current rank of the Crypto.com app")
    async def cryptocom_command(interaction: Interaction):

        average_sentiment_calculation = await weighted_average_sentiment_calculation()
        rank_number_cryptodotcom = await current_rank_cryptodotcom()
        now = datetime.now()
        current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

        sentiment_text, sentiment_image_filename = await evaluate_sentiment()
        change_symbol = await cryptodotcom_tracker.compare_ranks(rank_number_cryptodotcom)
        highest_rank, lowest_rank = await cryptodotcom_tracker.get_extreme_ranks()

        embed = Embed(title="Crypto.com Statistics", description="Real-time tracking and analysis of the Crypto.com app ranking.", color=0x1c64b0)
        file_thumb = File("assets/crypto-com-seeklogo.png", filename="cryptodotcom_logo.png")
        embed.set_thumbnail(url="attachment://cryptodotcom_logo.png")
        embed.add_field(name="🏆 Current Rank", value=f"#️⃣{number_to_emoji(rank_number_cryptodotcom)} in Finance on {current_datetime_hour}", inline=False)
        embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)
        if highest_rank:
            embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"#️⃣{number_to_emoji(highest_rank['rank'])} on {highest_rank['timestamp']}", inline=True)
        if lowest_rank:
            embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"#️⃣{number_to_emoji(lowest_rank['rank'])} on {lowest_rank['timestamp']}", inline=True)
        embed.add_field(name="🚥 Market Sentiment", value=f"Score: {average_sentiment_calculation}\nFeeling: {sentiment_text}", inline=False)
        file_sentiment = File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
        embed.set_image(url=f"attachment://{sentiment_image_filename}")
        avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
        embed.set_footer(text=f"Requested by {interaction.user.display_name}, {current_datetime_hour}.", icon_url=avatar_url if avatar_url else None)

        await cryptodotcom_tracker.save_rank(rank_number_cryptodotcom)
        await interaction.response.send_message(files=[file_thumb, file_sentiment], embed=embed)

    @bot.tree.command(name="set_alert", description="Set an alert for a specific crypto app rank change")
    @app_commands.describe(
        operator="The comparison operator for the alert (e.g., >, <, >=, <=)",
        rank="The rank threshold for the alert"
    )
    @app_commands.choices(
        app_name=[
            app_commands.Choice(name="Coinbase", value="coinbase"),
            app_commands.Choice(name="Coinbase wallet", value="cwallet"),
            app_commands.Choice(name="Crypto.com", value="cryptocom"),
            app_commands.Choice(name="Binance", value="binance")
        ],
        operator=[
            app_commands.Choice(name="greater than", value=">"),
            app_commands.Choice(name="less than", value="<"),
            app_commands.Choice(name="greater than or equal to", value=">="),
            app_commands.Choice(name="less than or equal to", value="<=")
        ]
    )
    async def set_alert_command(interaction: Interaction, app_name: str, operator: str, rank: int):
        alert_data = {
            'user_id': interaction.user.id,
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
                if (existing_alert['user_id'] == interaction.user.id and
                    existing_alert['app_name'] == app_name.lower() and
                    existing_alert['operator'] == operator and
                    existing_alert['rank'] == rank):
                    embed = Embed(description=f"❌ Alert for ``{app_name}`` when rank ``{operator} {rank}`` already exists.", color=0xff0000)
                    avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
                    embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=avatar_url if avatar_url else None)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
            
            # Add the new alert if no duplicates
            alerts.append(alert_data)
            with open('data/alerts.json', 'w') as f:
                json.dump(alerts, f, indent=4)

            embed = Embed(description=f"✅🔔 Alert set for {app_name} when rank ``{operator} {rank}``.", color=0x00ff00)
            avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=avatar_url if avatar_url else None)
            await interaction.response.send_message(embed=embed, ephemeral=False)

        except Exception as e:
            print(f"Failed to set or check alerts due to an error: {e}")
            await interaction.response.send_message("🚨 Failed to set alert due to an internal error.", ephemeral=True)
    
    @bot.tree.command(name="remove_alert", description="Remove an existing alert for a specific app")
    @app_commands.describe(app_name="The name of the application to remove the alert for")
    async def remove_alert_command(interaction: Interaction, app_name: str):
        if app_name is None:
            await send_error_message_remove_alert(interaction)
            return

        user_id = interaction.user.id
        alert_file_path = 'data/alerts.json'

        try:
            with open(alert_file_path, 'r+') as file:
                alerts = json.load(file)
                new_alerts = [alert for alert in alerts if not (alert['user_id'] == user_id and alert['app_name'].lower() == app_name.lower())]

                if len(alerts) == len(new_alerts):
                    embed = Embed(description=f"🙅‍♂️ No alert found for `{app_name.capitalize()}` that belongs to you.", color=Colour.red())
                else:
                    file.seek(0)
                    json.dump(new_alerts, file, indent=4)
                    file.truncate()
                    embed = Embed(description=f"🚮 Alert for `{app_name.capitalize()}` has been successfully removed.", color=Colour.green())

                embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except FileNotFoundError:
            embed = Embed(description="🚨 Alert data file not found.", color=Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except json.JSONDecodeError:
            embed = Embed(description="🚨 Error reading the alert data.", color=Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = Embed(description=f"🚨 Failed to remove the alert due to an error: {e}", color=Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="myalerts", description="Display your active alerts")
    async def myalerts_command(interaction: Interaction):
        user_id = interaction.user.id
        alert_file_path = 'data/alerts.json'  # Ensure the path is correct

        try:
            with open(alert_file_path, 'r') as file:
                alerts = json.load(file)
                user_alerts = [alert for alert in alerts if int(alert['user_id']) == user_id]

            if not user_alerts:
                embed = Embed(description="🤷‍♂️ You have no active alerts.", color=Colour.blue())
            else:
                embed = Embed(title="🔂🔔 Your Active Alerts", description="", color=Colour.green())
                for alert in user_alerts:
                    embed.add_field(name=f"✅ {alert['app_name'].title()} Alert",
                                    value=f"Trigger: {alert['operator']} {alert['rank']}",
                                    inline=False)

            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            await interaction.response.send_message(embed=embed, ephemeral=True)  # Make the message visible only to the user

        except FileNotFoundError:
            embed = Embed(description="🚨 Alert data file not found.", color=Colour.red())
            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except json.JSONDecodeError:
            embed = Embed(description="🚨 Error reading the alert data.", color=Colour.red())
            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = Embed(description=f"🚨 An error occurred while retrieving your alerts: {e}", color=Colour.red())
            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="remove_all_alerts", description="Remove all your set alerts")
    async def remove_all_alerts_command(interaction: Interaction):
        user_id = interaction.user.id
        try:
            # Load the current alerts from the file
            if os.path.exists('data/alerts.json'):
                with open('data/alerts.json', 'r') as file:
                    alerts = json.load(file)
                
                # Filter out alerts for the user to see if there are any
                user_alerts = [alert for alert in alerts if alert['user_id'] == user_id]

                if not user_alerts:
                    embed = Embed(description="🤷‍♂️ You have no alerts to remove.", color=Colour.blue())
                    embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

                # Remove all alerts for this user
                alerts = [alert for alert in alerts if alert['user_id'] != user_id]

                # Write the updated alerts back to the file
                with open('data/alerts.json', 'w') as file:
                    json.dump(alerts, file, indent=4)
                
                embed = Embed(title="🚮✅ Alerts Removed", description="All your alerts have been successfully removed.", color=0x00ff00)
                embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = Embed(description="🤷‍♂️ No alert file found or no alerts set.", color=Colour.blue())
                embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except json.JSONDecodeError as e:
            embed = Embed(description=f"🚨 Error reading the alert data: {str(e)}", color=0xff0000)
            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = Embed(description=f"🚨 Failed to remove alerts due to an error: {str(e)}", color=0xff0000)
            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="all_ranks", description="Display ranks and Data History of all crypto apps at once")
    async def all_ranks_command(interaction: Interaction):
        rank_tracker = RankTracker(bot)

        bitcoin_price = await get_bitcoin_price_usd()  
        bitcoin_emoji_id = "1234500592559194164"
        bitcoin_emoji = f"<:bitcoin:{bitcoin_emoji_id}>"
        bitcoin_price_text = f"``Current Bitcoin Price: 💲{bitcoin_price:,.2f} USD``" if bitcoin_price != "Unavailable" else f"{bitcoin_emoji} Bitcoin Price: Unavailable"

        embed = Embed(title="Crypto App Ranks", description="Current and historical ranks of major crypto apps.", color=0x4ba1da)
        embed.add_field(name=f"{bitcoin_emoji} Bitcoin Price", value=bitcoin_price_text, inline=False)

        apps = ["coinbase", "wallet", "binance", "cryptocom"]
        emoji_ids = {
            "coinbase": "<:coinbase_icon:1234492789967032330>",
            "wallet": "<:wallet_icon:1234492792320036925>",
            "binance": "<:binance_icon:1234492788616331295>",
            "cryptocom": "<:cryptocom_icon:1234492791355080874>"
        }

        # Fetch all ranks once to reduce repetitive calls
        logging.debug(f"Awaiting fetch_all_ranks")
        current_ranks = await rank_tracker.fetch_all_ranks()

        for idx, app in enumerate(apps):
            logging.debug(f"Awaiting get_historical_rank for {app} yesterday")
            yesterday_rank = await rank_tracker.get_historical_rank(app, days_back=1)
            last_week_rank = await rank_tracker.get_historical_rank(app, days_back=7)
            last_month_rank = await rank_tracker.get_historical_rank(app, months_back=1)

            current_rank = current_ranks[idx] if current_ranks[idx] is not None else "Unavailable"

            # Assuming yesterday_rank is an integer if it's not None
            change_text = "No data"
            if isinstance(current_rank, int) and isinstance(yesterday_rank, int):
                if current_rank < yesterday_rank:
                    change_icon = "🔼"  # Rank improved
                    change = yesterday_rank - current_rank
                elif current_rank > yesterday_rank:
                    change_icon = "🔻"  # Rank worsened
                    change = current_rank - yesterday_rank
                else:
                    change_icon = ""  # No change
                    change = ""
                change_text = f"{change_icon}{change}" if change_icon else "💤 No change"
            else:
                change_text = "Data unavailable"

            embed.add_field(
                name=f"{emoji_ids[app]} {app.capitalize()} Rank",
                value=f"``Current: #️⃣{number_to_emoji(current_rank)} ({change_text}) | Yesterday: #️⃣{number_to_emoji(yesterday_rank)} | Last Week: #️⃣{number_to_emoji(last_week_rank)} | Last Month: #️⃣{number_to_emoji(last_month_rank)}``",
                inline=False
            )

        await interaction.response.send_message(embed=embed)