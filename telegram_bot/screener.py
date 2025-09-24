import asyncio
import aiohttp
import numpy as np
import pandas as pd
import pandas_ta as ta
from aiogram import Bot, Dispatcher
from aiogram.utils import executor

# === НАСТРОЙКИ ===
API_KEY = "7707174304:AAH5i6cmFMEQaxD80R9OM0QbC_6J-PhdDmE"
CHAT_ID = "234878090"  # куда слать сигналы
BOT = Bot(token=API_KEY)
DP = Dispatcher(BOT)

GATE_API = "https://api.gateio.ws/api/v4"

# === ФУНКЦИИ ===
async def fetch_json(session, url):
    async with session.get(url) as resp:
        return await resp.json()

async def get_top_300_pairs(session):
    url = f"{GATE_API}/spot/tickers"
    data = await fetch_json(session, url)
    usdt_pairs = [x for x in data if x["currency_pair"].endswith("_USDT")]
    sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x["quote_volume"]), reverse=True)
    return [p["currency_pair"] for p in sorted_pairs[:300]]

async def get_candles(session, pair, interval="15m", limit=200):
    url = f"{GATE_API}/spot/candlesticks?currency_pair={pair}&interval={interval}&limit={limit}"
    data = await fetch_json(session, url)
    data = list(reversed(data))
    df = pd.DataFrame(data, columns=["t","o","c","h","l","v"])
    df["c"] = df["c"].astype(float)
    df["h"] = df["h"].astype(float)
    df["l"] = df["l"].astype(float)
    df["v"] = df["v"].astype(float)
    return df

def nearest_levels(highs, lows, left=5, right=5):
    supports, resistances = [], []
    for i in range(left, len(highs)-right):
        if lows[i] == min(lows[i-left:i+right]):
            supports.append(lows[i])
        if highs[i] == max(highs[i-left:i+right]):
            resistances.append(highs[i])
    return supports, resistances

def check_signal(df):
    df["rsi"] = ta.rsi(df["c"], length=14)
    last_rsi = df["rsi"].iloc[-1]
    price = df["c"].iloc[-1]
    highs = df["h"].values
    lows = df["l"].values

    supports, resistances = nearest_levels(highs, lows)
    nearest_sup = max([s for s in supports if s <= price], default=None)
    nearest_res = min([r for r in resistances if r >= price], default=None)

    signal = None
    if last_rsi < 30 and nearest_sup and abs(price - nearest_sup)/price < 0.01:
        signal = f"🟢 LONG: RSI={last_rsi:.1f}, цена около поддержки {nearest_sup:.4f}"
    elif last_rsi > 70 and nearest_res and abs(price - nearest_res)/price < 0.01:
        signal = f"🔴 SHORT: RSI={last_rsi:.1f}, цена около сопротивления {nearest_res:.4f}"
    return signal

async def scan_market():
    async with aiohttp.ClientSession() as session:
        pairs = await get_top_300_pairs(session)
        results = []
        for pair in pairs:
            try:
                df = await get_candles(session, pair)
                sig = check_signal(df)
                if sig:
                    results.append((pair, sig))
            except Exception as e:
                print(f"Ошибка {pair}: {e}")
        return results

async def job():
    while True:
        print("🔍 Проверка топ-300 монет Gate.io...")
        signals = await scan_market()
        if signals:
            for pair, sig in signals:
                text = f"📊 {pair}\n{sig}"
                await BOT.send_message(CHAT_ID, text)
        else:
            print("Сигналов нет.")
        await asyncio.sleep(15*60)  # каждые 15 минут

# === СТАРТ ===
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(job())
    from aiogram import executor
    executor.start_polling(DP, skip_updates=True)
