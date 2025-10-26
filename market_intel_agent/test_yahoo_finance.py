from tools.yahoo_finance_tool import YahooFinanceTool
from utils.logger import AgentLogger


def main():
    logger = AgentLogger(log_dir='test_websearch')
    tool = YahooFinanceTool(logger=logger)
    ticker = "AAPL"

    print(f"\nTesting YahooFinanceTool for {ticker}")
    quote = tool.get_quote(ticker)
    print("Quote:", quote)

    profile = tool.get_company_profile(ticker)
    print("Profile:", {k: profile.get(k) for k in ["name", "sector", "industry", "website"]})

    news = tool.get_news(ticker, count=3)
    print("News:")
    for i, item in enumerate(news):
        print(f"  {i+1}. {item.get('title')} ({item.get('publisher')})\n     {item.get('link')}")


if __name__ == "__main__":
    main()