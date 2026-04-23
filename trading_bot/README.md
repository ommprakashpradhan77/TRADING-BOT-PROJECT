<div align="center">

# 🚀 Binance Futures Testnet Trading Bot
**A lightweight, robust, and interactive CLI application for Binance USDT-M Futures.**

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Binance](https://img.shields.io/badge/Binance-Futures_Testnet-F3BA2F?style=for-the-badge&logo=binance&logoColor=black)
![Architecture](https://img.shields.io/badge/Architecture-Clean-success?style=for-the-badge)

</div>

---

<p align="center">
  A simplified Python application built explicitly to place orders on the <b>Binance Futures Testnet</b> without the bloat of massive external Binance wrappers, powered directly by raw REST APIs.
</p>

## ✨ Key Features

* 🛒 **Multiple Order Types**: Full support for `MARKET`, `LIMIT`, and bonus `STOP_MARKET` types.
* 🔄 **Bidirectional**: Easily execute `BUY` or `SELL` positions.
* 🛡️ **Clean Architecture**: Deeply separated concerns. Validations, network clients, order logic, and presentation all live in harmony.
* 💻 **Stunning Interactive CLI**: Built with `Typer` & `Rich`! Enjoy gorgeous terminal tables, smart argument prompting, and bright status outputs.
* 🪵 **Granular Logging**: Intelligently logs API footprints, JSON payloads, and HTTP errors directly to `bot.log`.
* ⏱️ **Auto Time-Sync**: Automatically handles Binance's infamous `Timestamp` drift errors via pre-trade sync offsets!

---

## 🛠️ Installation & Setup

### 1. Requirements & Dependencies
Ensure you have Python 3.8+ installed, and then initialize the project requirements:

```bash
pip install -r requirements.txt
```

### 2. Connect Your Testnet Credentials
> **Note**: You must have an active [Binance Futures Testnet](https://testnet.binancefuture.com) account.

1. Create a `.env` file in the main folder (or simply copy `.env.example`).
2. Insert your newly generated API Keys:
```env
BINANCE_API_KEY=aWU4w0E1AJLFuYozYu6BwJkISrgWHHtjjTA2PYGmr8f81NJ9sZQpRSkc1qMzpe4w
BINANCE_API_SECRET=OIgUztylXxraEcWF5ebt9vDEYZmb9iHpoXvAGJ0O5GrkA8hLobGPAQEpGJyAgvqW
```

---

## 🎮 How to Use the Bot

You have the choice of two amazing operational modes: **Interactive** or **Headless CLI**.

### 🌟 Mode 1: Interactive Wizard (Recommended)
Don't want to type long commands? Use the interactive wizard which gracefully guides you through your trades!

```bash
python cli.py --interactive
```

### ⚡ Mode 2: Explicit Command Line
Perfect for running via scripts or power-users who want instant executions.

> **Place a Market Order**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.005
```

> **Place a Limit Order**
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 1.0 --price 1800.0
```

> **Place a Stop Market Order** *(Triggers a market jump at specified price)*
```bash
python cli.py --symbol SOLUSDT --side SELL --type STOP_MARKET --quantity 5.0 --stop-price 20.0
```

*Need a quick refresher? Run `python cli.py --help` at any time!*

---

## 📁 Project Structure

```text
trading_bot/
├── 🤖 bot/
│   ├── __init__.py
│   ├── client.py         # The HTTP REST Engine & Time Sync
│   ├── logging_config.py # Log generation configuration
│   ├── orders.py         # Payload configurations for orders
│   └── validators.py     # Pre-flight input validations
├── 📄 .env               # Your absolute secrets!
├── 📜 bot.log            # Running audit footprint
├── 💻 cli.py             # User terminal entry-point
└── 📦 requirements.txt   # Core Dependencies
```

---

## 📌 Architectural Assumptions

* **Target Network**: Directed strictly at `https://testnet.binancefuture.com` (USDT-M Futures).
* **Logging Policy**: Automatically stamps and records all raw outputs sequentially in `bot.log`.
* **Execution Parameters**:
  * `LIMIT` orders are universally stamped with a `GTC` (Good Till Cancelled) TimeInForce format.
  * `STOP_MARKET` is engineered as a standard market-trigger rather than a complex stop-limit.
