import requests
import aiohttp
from data_management.database import AppRankTracker
from bs4 import BeautifulSoup

def current_rank_coinbase():
    url = "https://apps.apple.com/us/app/coinbase-buy-bitcoin-ether/id886427730"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    rank_element = soup.find('a', class_='inline-list__item', href=True, text=lambda t: 'in Finance' in t)
    if rank_element:
        rank_text = rank_element.get_text(strip=True)
        return ''.join(filter(str.isdigit, rank_text))
    return None

def current_rank_wallet():
    url = "https://apps.apple.com/us/app/coinbase-wallet-nfts-crypto/id1278383455"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    rank_element = soup.find('a', class_='inline-list__item', href=True, text=lambda t: 'in Finance' in t)
    if rank_element:
        rank_text = rank_element.get_text(strip=True)
        return ''.join(filter(str.isdigit, rank_text))
    return None

def current_rank_binance():
    url = "https://apps.apple.com/us/app/binance-us-buy-bitcoin-eth/id1492670702"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    rank_element = soup.find('a', class_='inline-list__item', href=True, text=lambda t: 'in Finance' in t)
    if rank_element:
        rank_text = rank_element.get_text(strip=True)
        return ''.join(filter(str.isdigit, rank_text))
    return None

def current_rank_cryptodotcom():
    url = "https://apps.apple.com/us/app/crypto-com-buy-bitcoin-sol/id1262148500"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    rank_element = soup.find('a', class_='inline-list__item', href=True, text=lambda t: 'in Finance' in t)
    if rank_element:
        rank_text = rank_element.get_text(strip=True)
        return ''.join(filter(str.isdigit, rank_text))
    return None

async def get_bitcoin_price_usd():
    """Fetch the current price of Bitcoin in USD from the CoinGecko API asynchronously."""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=USD"
    try:
        # Use aiohttp client session to make the HTTP request
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  # This will raise an aiohttp.ClientResponseError if the HTTP request returned an unsuccessful status code
                data = await response.json()
                bitcoin_price = data['bitcoin']['usd']
                return bitcoin_price
    except aiohttp.ClientResponseError as e:
        print(f"HTTP request failed: {e}")
        return "Unavailable"
    except Exception as e:
        print(f"Failed to fetch Bitcoin price: {e}")
        return "Unavailable"