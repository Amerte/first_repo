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

    return all_bids, all_asks

# --- строим график ---
def plot_orderbook(bids, asks, symbol):
    if not bids or not asks:
        return None

    # --- берём 20 крупнейших покупок и продаж ---
    top_bids = sorted(bids.items(), key=lambda x: x[1], reverse=True)[:20]
    top_asks = sorted(asks.items(), key=lambda x: x[1], reverse=True)[:20]

    # сортировка для наглядности
    top_bids_sorted = [top_bids[0]] + sorted(top_bids[1:], key=lambda x: x[0], reverse=True)
    top_asks_sorted = sorted(top_asks[:-1], key=lambda x: x[0]) + [top_asks[-1]]

    plot_prices = [p for p,_ in top_bids_sorted] + [p for p,_ in top_asks_sorted]
    plot_volumes = [v for _,v in top_bids_sorted] + [v for _,v in top_asks_sorted]
    colors = ["green"]*len(top_bids_sorted) + ["red"]*len(top_asks_sorted)

    plt.figure(figsize=(14,7))
    plt.bar(range(len(plot_prices)), plot_volumes, color=colors)

    xticks_pos = list(range(len(plot_prices)))
    xticks_labels = [str(p) for p in plot_prices]

    plt.xticks(xticks_pos, xticks_labels, rotation=45)
    plt.title(f"Orderbook {symbol}")
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
        # автоматически добавляем USDT
        if not text.endswith("USDT"):
            symbol = text + "USDT"
        else:
            symbol = text

        bids, asks = fetch_orderbooks(symbol)

        logger.info(f"Symbol: {symbol}")
        logger.info(f"Bids sample: {list(bids.items())[:5]}, Asks sample: {list(asks.items())[:5]}")

        if not bids or not asks:
            await update.message.reply_text("Нет данных по этому символу.")
            return

        file = plot_orderbook(bids, asks, symbol)
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
