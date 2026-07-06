# Binance Futures Testnet Trading Bot

This is a simple command-line application that places **Market** and **Limit** orders on the Binance Futures Testnet. The project was built in Python with a focus on clean structure, input validation, logging, and error handling.

## Project Structure

```
trading_bot/
bot/
    client.py            # Binance API client
    orders.py            # Order placement logic
    validators.py        # Input validation
    logging_config.py    # Logging setup

cli.py                   # Command-line entry point
requirements.txt
README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Swati668/Binance-Futures-Testnet-Trading-Bot.git
cd trading_bot
```

### 2. Create and activate a virtual environment (optional but recommended)

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API credentials

Create a `.env` file in the project root and add your Binance Futures Testnet credentials.

```env
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
BASE_URL=https://testnet.binancefuture.com
```

---

## How to Run

### Market Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.005
```

### Limit Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.005 --price 95000
```

After running a command, the application displays the order summary and Binance response in the terminal. API requests, responses, and any errors are also written to the log file.

---

## Assumptions

- The application is intended to work only with the **Binance Futures Testnet**.
- Valid Testnet API credentials are available and configured in the `.env` file.
- A price must be provided when placing a **LIMIT** order.
- A price is not required for **MARKET** orders.
- The trading pair used (for example, `BTCUSDT`) exists on the Binance Futures Testnet.