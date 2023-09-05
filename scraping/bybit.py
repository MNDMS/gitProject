import requests
import asyncio
import nest_asyncio
from datetime import datetime, timedelta
from telegram import Bot

nest_asyncio.apply()

BOT_TOKEN = '6593706311:AAGfep182h5A1hOifip4095pVEy4Rp7kZTs'
CHAT_ID = "@roofpocazz"
symbols = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'LTCUSDT', 'ADAUSDT', 'SOLUSDT', 'LINKUSDT', 'XMRUSDT']

def get_current_price(symbol):
    url = f'https://api.bybit.com/v2/public/tickers'
    params = {'symbol': symbol}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        try:
            data = response.json()
            if 'result' in data:
                price = data['result'][0]['last_price']
                return price
        except Exception as e:
            print('Error processing response:', e)
            print(response.content)
    else:
        print(f'Failed to fetch data for {symbol}. Status code: {response.status_code}')
        return None

async def send_telegram_message(message):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

async def fetch_and_send_prices():
    gmt_plus_6_time = datetime.utcnow() + timedelta(hours=6)
    message = f'BYBIT: Prices at {gmt_plus_6_time.strftime("%Y-%m-%d %H:%M:%S")} (GMT+6):\n\n'
    
    for symbol in symbols:
        price = get_current_price(symbol)
        if price is not None:
            formatted_price = f'{float(price):.2f}'
            message += f'{symbol}: {formatted_price}\n'
    
    await send_telegram_message(message)

async def main():
    await fetch_and_send_prices()

if __name__ == "__main__":
    asyncio.run(main())
