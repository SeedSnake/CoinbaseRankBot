from api.apps import current_rank_binance, current_rank_coinbase, current_rank_cryptodotcom, current_rank_wallet

def number_to_emoji(number):
    digit_to_emoji = {
        '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣',
        '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣'
    }
    try:
        # Ensure the number can be converted to a string of digits
        # This will also validate that it's possible to iterate over the string
        return ''.join(digit_to_emoji[digit] for digit in str(number))
    except KeyError as e:
        # If a KeyError occurs, it means 'number' contained a non-digit character
        print(f"Non-digit character encountered: {e}")
        return None
    except Exception as e:
        # Catch any other exceptions that might occur
        print(f"An error occurred: {e}")
        return None

def evaluate_sentiment():
    # Fetch the current ranks
    coinbase_current_rank = current_rank_coinbase()
    wallet_current_rank = current_rank_wallet()
    binance_current_rank = current_rank_binance()
    cryptodotcom_current_rank = current_rank_cryptodotcom()

    # Check if either rank is None
    if None in (coinbase_current_rank, wallet_current_rank, binance_current_rank, cryptodotcom_current_rank):
        print("Debug: One or both ranks are None.")
        return "No data available for sentiment analysis.", None

    try:
        # Ensure ranks are integers for calculation
        coinbase_current_rank = int(coinbase_current_rank)
        wallet_current_rank = int(wallet_current_rank)
        binance_current_rank = int(binance_current_rank)
        cryptodotcom_current_rank = int(cryptodotcom_current_rank)
        
        # Calculate weighted average
        weighted_average_rank = 100 - (5 * (coinbase_current_rank + cryptodotcom_current_rank) + 2.5 * binance_current_rank + wallet_current_rank) / 13.5
        
        # Evaluate sentiment based on the weighted average
        sentiment, image_file = evaluate_based_on_weighted_average(weighted_average_rank)

        return sentiment, image_file

    except TypeError as e:
        print(f"Error in evaluate_sentiment: {e}")
        return "Error processing rank values.", None

    except ValueError as e:
        print(f"Error converting rank values to integers: {e}")
        return "Error processing rank values.", None

def evaluate_based_on_weighted_average(weighted_average_rank):
    if weighted_average_rank >= 90:
        sentiment = "🟢🟢🟢 Extreme Greed!"
    elif weighted_average_rank >= 80:
        sentiment = "🟢🟢 Greed!"
    elif weighted_average_rank >= 75:
        sentiment = "🟢 Optimism"
    elif weighted_average_rank >= 70:
        sentiment = "🟡 Doubt"
    elif weighted_average_rank >= 65:
        sentiment = "🟠 Anxiety"
    elif weighted_average_rank >= 50:
        sentiment = "🔴🔴 Fear!"
    else:
        sentiment = "🔴🔴🔴 Capitulation!"

    sentiment_images = {
        "🟢🟢🟢 Extreme Greed!": "extreme_greed.png",
        "🟢🟢 Greed!": "greed.png",
        "🟢 Optimism": "optimism.png",
        "🟡 Doubt": "doubt.png",
        "🟠 Anxiety": "anxiety.png",
        "🔴🔴 Fear!": "fear.png",
        "🔴🔴🔴 Capitulation!": "capitulation.png"
    }
    
    image_file = sentiment_images.get(sentiment)
    return sentiment, image_file

def weighted_average_sentiment_calculation():

    rank_number_coinbase = int(current_rank_coinbase())
    rank_number_binance = int(current_rank_binance())
    rank_number_wallet = int(current_rank_wallet())
    rank_number_cryptocom = int(current_rank_cryptodotcom())

    weighted_average_rank = (5 * (rank_number_coinbase + rank_number_cryptocom) + 2.5 * rank_number_binance + rank_number_wallet) / 13.5

    return 100 - round(weighted_average_rank)

print(weighted_average_sentiment_calculation())