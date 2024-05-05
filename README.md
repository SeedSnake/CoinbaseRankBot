# CryptoAppIndex

<p align="center">
<a href="https://imgbb.com/"><img src="https://i.ibb.co/4sLW3yM/Crypto-App-Index-Logo2.png" alt="Crypto-App-Index-Logo2" border="0"></a>
</p>

**ℹ The project is still under development, with many features yet to come. The bot will not always be online until its final version is released. For more information, please contact me. :)**

CryptoAppIndex is a Discord bot designed to provide real-time ranking of crypto apps on the App Store directly within your Discord server. 
By using a simple command, users can quickly get up-to-date information about Crypto's apps popularity, live positional change, ranks data history, and market sentiment.

When crypto apps rank among the most downloaded, it may signal significant market greed!
You can monitor these trends and set alerts for ranking changes, ensuring you are always informed about potential market opportunities.

<a href="https://github.com/SeedSnake/CryptoAppIndex/releases/"><img src="https://img.shields.io/github/tag/SeedSnake/CryptoAppIndex?include_prereleases=&sort=semver&color=blue" alt="GitHub tag"></a> <a href="#license"><img src="https://img.shields.io/badge/License-GNU-blue" alt="License"></a> <img src="https://img.shields.io/badge/maintained-yes-blue" alt="maintained - yes">


## Features

- **Fetch Ranking**: Sends the current ranking of most popular crypto apps (Coinbase, Binance, Crypto.com) on the App Store with simple commands.
- **Automatic Updates**: The bot fetches the most recent data with each command, ensuring the information is always up to date.
- **Daily Monitoring**: Compare the current ranking with that of the day before and indicates the evolution.
- **Market Sentiment**: Analyze the leaderboard to provide market sentiment using a weighted average of crypto apps' rankings. (Extreme Greed, Greed, Optimism, Doubt, etc.).
- **Rank Records**: The bot tracks the highest and lowest ranks achieved by crypto apps, providing a long-term perspective on their performance in the App Store.
- **Alerts Commands**: You can set alert thresholds for your applications. Receive direct messages when the app's rank meets your specified conditions with !alert.
- **Live Status Updates**: The bot continuously updates its status to show the current ranks of tracked applications, providing real-time insights directly in its Discord status.

<p align="center">
<a href="https://ibb.co/0qRTQnp"><img src="https://i.ibb.co/gyLN6rb/MOCKUP-CRPTOAPPINDEX.png" alt="MOCKUP-CRPTOAPPINDEX" border="0"></a>
</p>

## Installation

Click on the invitation below (The bot will be up soon! 🔜👀):

<a href=""><img src="https://img.shields.io/badge/Discord-Invitation-7289DA?style=for-the-badge&logo=discord&logoColor=white" alt="Discord - Invitation"></a>

## Usage

After integrating CryptoAppIndex onto your server, you can utilize the following commands to access the current rankings of various crypto apps and the global market sentiment using a weighted average:

- Use <code>!coinbase</code> to retrieve the current ranking and all-time highest achieved rank of the Coinbase app.
- Use <code>!cwallet</code> to retrieve the current ranking and all-time highest achieved rank of Coinbase's Wallet app.
- Use <code>!binance</code> to retrieve the current ranking and all-time highest achieved rank of the Binance app.
- Use <code>!cryptocom</code> to retrieve the current ranking and all-time highest achieved rank of the Crypto.com app.

<p align="center"><a href="https://imgbb.com/"><img src="https://i.ibb.co/Yty3qPN/c.png" alt="coinbase_command" border="0"></a></p>
  
- <code>!ranks</code> : Provides a comprehensive view of all the current crypto app rankings, historical data for all monitored crypto apps, and the current Bitcoin price with a single command.

<p align="center"><a href="https://imgbb.com/"><img src="https://i.ibb.co/6yK3XQZ/r.png" alt="ranks_command" border="0"></a></p>

Alerts Management: 

- <code>!alert /app-name/ /operator/ /rank/</code> : Set alert with condition.
- <code>!myalerts</code> : Display your current alerts.
- <code>!rmalert /app-name/</code> and <code>!rmall</code> : Delete one or all alerts.

## License

CryptoAppIndex is distributed under the GNU General Public License v3.0. For more information, see the `LICENSE` file in the project repository.

## Legal Information

CryptoAppIndex is designed solely to retrieve and display the ranking information of specific applications such as Coinbase, Binance, Crypto.com, and Coinbase Wallet from publicly accessible sources. The data provided by this bot is for informational purposes only and should not be interpreted as an endorsement or reflection of the views of the applications concerned or any affiliated platforms, including the App Store. 

Users are advised that all interpretations and actions based on the bot's data are at their own discretion and risk. Importantly, this bot does not provide investment advice, nor should its output be used as a basis for making investment decisions.
