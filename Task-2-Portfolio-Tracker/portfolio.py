
import csv
import yfinance as yf

# Load S&P 500 dataset
companies = {}

with open("constituents.csv", "r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        symbol = row["Symbol"].strip().upper()
        companies[symbol] = row["Security"]


# Store portfolio positions in a dictionary
portfolio = {}

print("\n===== INVESTMENT PORTFOLIO TRACKER =====")

while True:
    ticker = input("\nEnter stock ticker (e.g. AAPL): ").strip().upper()

    # Validate ticker using dataset
    if ticker not in companies:
        print("Invalid ticker! Please enter an S&P 500 ticker.")
        continue

    if ticker in portfolio:
        print("This stock is already in your portfolio.")
        continue

    try:
        buy_price = float(input("Enter buying price per share: "))
        quantity = int(input("Enter number of shares: "))

        if buy_price <= 0 or quantity <= 0:
            print("Price and quantity must be greater than zero.")
            continue

        # Fetch latest available stock price
        stock = yf.Ticker(ticker)
        history = stock.history(period="5d")

        if history.empty:
            print("Unable to fetch stock price. Try again.")
            continue

        current_price = float(history["Close"].dropna().iloc[-1])

        if current_price <= 0:
            print("Invalid market price received.")
            continue

        portfolio[ticker] = {
            "company": companies[ticker],
            "buy_price": buy_price,
            "quantity": quantity,
            "current_price": current_price
        }

        print(f"{ticker} added successfully!")
        print(f"Latest available price: ${current_price:.2f}")

    except ValueError:
        print("Please enter valid numeric values.")
        continue
    except Exception as error:
        print("Error fetching stock data:", error)
        continue

    another = input("Add another stock? (yes/no): ").strip().lower()

    if another != "yes":
        break


# Calculate portfolio summary
total_invested = 0
total_value = 0

print("\n========== PORTFOLIO SUMMARY ==========")

for ticker, data in portfolio.items():

    invested = data["buy_price"] * data["quantity"]
    market_value = data["current_price"] * data["quantity"]

    profit_loss = market_value - invested
    percentage = (profit_loss / invested) * 100

    total_invested += invested
    total_value += market_value

    print(f"\nStock: {ticker}")
    print(f"Company: {data['company']}")
    print(f"Invested: ${invested:.2f}")
    print(f"Current Value: ${market_value:.2f}")
    print(f"Gain/Loss: ${profit_loss:.2f}")
    print(f"Percentage: {percentage:.2f}%")


total_profit_loss = total_value - total_invested

print("\n========== TOTAL PORTFOLIO ==========")
print(f"Total Invested: ${total_invested:.2f}")
print(f"Total Market Value: ${total_value:.2f}")
print(f"Total Gain/Loss: ${total_profit_loss:.2f}")


# Export results to CSV
with open("portfolio_summary.csv", "w", newline="", encoding="utf-8") as file:

    fieldnames = [
        "Ticker", "Company", "Buy Price", "Quantity",
        "Current Price", "Invested Amount",
        "Current Value", "Profit/Loss", "Percentage"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for ticker, data in portfolio.items():

        invested = data["buy_price"] * data["quantity"]
        market_value = data["current_price"] * data["quantity"]
        profit_loss = market_value - invested
        percentage = (profit_loss / invested) * 100

        writer.writerow({
            "Ticker": ticker,
            "Company": data["company"],
            "Buy Price": data["buy_price"],
            "Quantity": data["quantity"],
            "Current Price": data["current_price"],
            "Invested Amount": invested,
            "Current Value": market_value,
            "Profit/Loss": profit_loss,
            "Percentage": percentage
        })

print("\nPortfolio summary saved to portfolio_summary.csv")
