import requests
import asyncio
import nest_asyncio
from datetime import datetime, timedelta
from telegram import Bot

nest_asyncio.apply()

BOT_TOKEN = '6593706311:AAGfep182h5A1hOifip4095pVEy4Rp7kZTs'
CHAT_ID = "@roofpocazz"
symbols = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'LTCUSDT', 'ADAUSDT', 'SOLUSDT', 'LINKUSDT', 'XMRUSDT']

def get_currencies():

    url = 'https://api.bybit.com/v2/public/tickers'

    response = requests.get(url)
    
    if response.status_code == 200:

        data = response.json()
        nums = list(range(len(data['result'])))

        symbols_list = []
        prices_list = []

        for n in nums:
            sb = data['result'][n]['symbol']
            lp = data['result'][n]['last_price']

            symbols_list.append(sb)
            prices_list.append(lp)

        sym_pr = dict(zip(symbols_list, prices_list))

        sp = {key: sym_pr[key] for key in symbols}

        return sp
    
    else:
        print(response.status_code)
        sp = {'B' : 1}
        return sp

def get_message():

    gmt_plus_6_time = datetime.utcnow() + timedelta(hours=6)
    message = f'BYBIT: Prices at {gmt_plus_6_time.strftime("%Y-%m-%d %H:%M:%S")} (GMT+6):\n\n'

    for s, p in get_currencies().items():
        message += f'{s}: {p}\n'
    
    return message

async def send_message():
    
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text= get_message())

if __name__ == "__main__":
    asyncio.run(send_message())
