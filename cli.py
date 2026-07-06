import argparse
import sys
from bot.logging_config import setup_logging
from bot.validators import validate_inputs
from bot.client import BinanceFuturesClient

def main():
    logger = setup_logging()
    
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Simplified Trading Bot")
    parser.add_argument("--symbol", required=True, help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL", "buy", "sell"], help="Order side")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT", "market", "limit"], help="Order Type")
    parser.add_argument("--quantity", required=True, type=float, help="Quantity to trade")
    parser.add_argument("--price", type=float, help="Price (Required if order type is LIMIT)")

    args = parser.parse_args()

    # Input Validation
    try:
        validate_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )
    except ValueError as e:
        logger.error(f"Validation Error: {e}")
        print(f"\n Validation Error: {str(e)}")
        sys.exit(1)

    # Order execution Summary Printout
    print("\n=== Order Request Summary ===")
    print(f"Symbol:   {args.symbol.upper()}")
    print(f"Side:     {args.side.upper()}")
    print(f"Type:     {args.type.upper()}")
    print(f"Quantity: {args.quantity}")
    if args.price:
        print(f"Price:    {args.price}")
    print("=============================\n")

    # Fire Client API Request
    try:
        client = BinanceFuturesClient(logger)
        success, response = client.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )
        
        print("=== Order Response Details ===")
        if success:
            print("Status: SUCCESS(Order placed successfully)")
            print(f"OrderId:      {response.get('orderId')}")
            print(f"Status Msg:   {response.get('status')}")
            print(f"Executed Qty: {response.get('executedQty')}")
            print(f"Avg Price:    {response.get('avgPrice', 'N/A')}")
        else:
            print("Status: FAILED(Order placement failed)")
            print(f"Error Msg:    {response.get('msg', response.get('error'))}")
        print("=============================\n")
        
    except Exception as e:
        logger.critical(f"Unhandled Exception: {str(e)}")
        print(f"\nCritical Error: {e}")

if __name__ == "__main__":
    main()