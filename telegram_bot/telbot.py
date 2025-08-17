import logging
import requests
import matplotlib
matplotlib.use('Agg')  # Без GUI
import matplotlib.pyplot as plt
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# --- настройки ---
TELEGRAM_TOKEN = "7707174304:AAH5i6cmFMEQaxD80R9OM0QbC_6J-PhdDmE"
EXCHANGES = ["binance", "okx", "bybit", "gate", "mexc"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- функция корректировки символа ---
def format_symbol_for_exchange(symbol: str, exchange: str) -> str:
    s = symbol.upper()
    if exchange in ["binance", "bybit", "mexc"]:
        return s.replace("-", "").replace("_", "")
    elif exchange == "okx":
        return s.replace("_","-")
    elif exchange == "gate":
        return s.replace("-", "_")
    return s

# --- функции API ---
def get_binance(symbol: str):
    url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=100"
    r = requests.get(url, timeout=10).json()
    return r.get("bids", []), r.get("asks", [])

def get_okx(symbol: str):
    url = f"https://www.okx.com/api/v5/market/books?instId={symbol}&sz=100"
    r = requests.get(url, timeout=10).json()
    data = r.get("data", [{}])[0]
    return data.get("bids", []), data.get("asks", [])

def get_bybit(symbol: str):
    url = f"https://api.bybit.com/v5/market/orderbook?category=spot&symbol={symbol}&limit=100"
    r = requests.get(url, timeout=10).json()
    data = r.get("result", {}).get("a", []), r.get("result", {}).get("b", [])
    return data[1], data[0]

def get_gate(symbol: str):
    url = f"https://api.gateio.ws/api/v4/spot/order_book?currency_pair={symbol}&limit=100"
    r = requests.get(url, timeout=10).json()
    return r.get("bids", []), r.get("asks", [])

def get_mexc(symbol: str):
    url = f"https://api.mexc.com/api/v3/depth?symbol={symbol}&limit=100"
    r = requests.get(url, timeout=10).json()
    return r.get("bids", []), r.get("asks", [])

# --- агрегируем ордербуки ---
def fetch_orderbooks(symbol: str):
    all_bids = {}
    all_asks = {}

    for ex in EXCHANGES:
        try:
            sym = format_symbol_for_exchange(symbol, ex)
            if ex == "binance":
                bids, asks = get_binance(sym)
            elif ex == "okx":
                bids, asks = get_okx(sym)
            elif ex == "bybit":
                bids, asks = get_bybit(sym)
            elif ex == "gate":
                bids, asks = get_gate(sym)
            elif ex == "mexc":
                bids, asks = get_mexc(sym)
            else:
                continue

            for p, v in bids:
                all_bids[float(p)] = all_bids.get(float(p), 0) + float(v)
            for p, v in asks:
                all_asks[float(p)] = all_asks.get(float(p), 0) + float(v)

        except Exception as e:
            logger.warning(f"{ex} error: {e}")

    best_bid = max(all_bids.keys()) if all_bids else None
    best_ask = min(all_asks.keys()) if all_asks else None

    return all_bids, all_asks, best_bid, best_ask

# --- строим график ---
def plot_orderbook(bids, asks, symbol, timeframe):
    if not bids or not asks:
        return None

    # --- берём 3 самых больших объёма ---
    top_bids = sorted(bids.items(), key=lambda x: x[1], reverse=True)[:3]
    top_asks = sorted(asks.items(), key=lambda x: x[1], reverse=True)[:3]

    # --- создаём данные для графика ---
    prices = [p for p,_ in top_bids] + [p for p,_ in top_asks]
    volumes = [v for _,v in top_bids] + [v for _,v in top_asks]
    colors = ["green"]*3 + ["red"]*3

    plt.figure(figsize=(10,6))

    # рисуем вертикальные линии
    for i, price in enumerate(prices):
        plt.vlines(x=price, ymin=0, ymax=volumes[i], color=colors[i], linewidth=5)

    # подписи цен только под линиями
    plt.xticks(prices, [str(round(p,2)) for p in prices], rotation=45)
    plt.title(f"Orderbook {symbol} ({timeframe})")
    plt.xlabel("Цена")
    plt.ylabel("Объем")
    plt.tight_layout()

    filename = "orderbook.png"
    plt.savefig(filename)
    plt.close()
    return filename


# --- обработчик сообщений ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip().upper()
        parts = text.split()
        if len(parts) != 2:
            await update.message.reply_text("Формат: BTCUSDT 1h")
            return

        symbol, timeframe = parts
        bids, asks, best_bid, best_ask = fetch_orderbooks(symbol)

        logger.info(f"Symbol: {symbol}")
        logger.info(f"Bids sample: {list(bids.items())[:5]}, Asks sample: {list(asks.items())[:5]}")
        logger.info(f"Best Bid: {best_bid}, Best Ask: {best_ask}")

        if not bids or not asks or best_bid is None or best_ask is None:
            await update.message.reply_text("Нет данных по этому символу.")
            return

        file = plot_orderbook(bids, asks, symbol, timeframe, best_bid, best_ask)
        if file is None or not os.path.exists(file):
            await update.message.reply_text("Ошибка при построении графика.")
            return

        with open(file, "rb") as f:
            await update.message.reply_photo(photo=f)

        os.remove(file)

    except Exception as e:
        logger.error(e)
        await update.message.reply_text(f"Ошибка при обработке запроса: {e}")

# --- запуск бота ---
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
