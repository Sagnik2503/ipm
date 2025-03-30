# from crewai.tools import BaseTool
# from typing import Type
# from pydantic import BaseModel, Field
# import yfinance as yf
# import pandas as pd
# import json
# from datetime import datetime

# class FetchStockDataInput(BaseModel):
#     """Input schema for FetchStockDataTool."""
#     ticker: str = Field(..., description="The stock ticker symbol (e.g., 'AAPL').")
#     data_type: str = Field(
#         "current",
#         description="The type of data to fetch: 'current', 'historical', 'info', 'dividends', 'earnings', 'pe_ratio', or 'news'.",
#     )
#     start_date: str = Field(
#         None, 
#         description="Start date for historical data (YYYY-MM-DD). Required if data_type is 'historical'."
#     )
#     end_date: str = Field(
#         None, 
#         description="End date for historical data (YYYY-MM-DD). Required if data_type is 'historical'."
#     )
#     format: str = Field(
#         "text",
#         description="Output format: 'text' (default) or 'json'."
#     )

# class FetchStockDataTool(BaseTool):
#     name: str = "fetch_stock_data"
#     description: str = (
#         "Fetches stock data using yfinance. This includes current price, historical data, company info, dividends, earnings, P/E ratio, or news for a given stock ticker."
#     )
#     args_schema: Type[BaseModel] = FetchStockDataInput

#     def _run(self, ticker: str, data_type: str = "current", start_date: str = None, end_date: str = None, format: str = "text") -> str:
#         try:
#             stock = yf.Ticker(ticker)
#             result = {}

#             if data_type == "current":
#                 history = stock.history(period="1d")
#                 if history.empty:
#                     return f"No recent trading data available for {ticker}."
#                 current_price = history['Close'].iloc[-1]
#                 result = {"ticker": ticker, "current_price": round(current_price, 2)}

#             elif data_type == "historical":
#                 if not start_date or not end_date:
#                     return "Start date and end date are required for historical data."
                
#                 start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
#                 end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')

#                 historical_data = stock.history(start=start_date, end=end_date)
#                 if historical_data.empty:
#                     return f"No historical data found for {ticker} from {start_date} to {end_date}."
#                 result = {"ticker": ticker, "historical_data": historical_data.to_json()}

#             elif data_type == "info":
#                 result = {"ticker": ticker, "info": stock.info or "No data available"}

#             elif data_type == "dividends":
#                 dividends = stock.dividends
#                 result = {"ticker": ticker, "dividends": dividends.to_json() if not dividends.empty else "No dividends data available."}

#             elif data_type == "earnings":
#                 earnings = stock.earnings
#                 result = {"ticker": ticker, "earnings": earnings.to_json() if not earnings.empty else "No earnings data available."}

#             elif data_type == "pe_ratio":
#                 pe_ratio = stock.info.get("trailingPE", "N/A")
#                 result = {"ticker": ticker, "pe_ratio": pe_ratio}

#             elif data_type == "news":
#                 news = [{"title": f"Latest news for {ticker}", "date": datetime.now().isoformat(), "content": "Market news..."}]
#                 result = {"ticker": ticker, "news": news}

#             else:
#                 return f"Invalid data_type '{data_type}'. Options: 'current', 'historical', 'info', 'dividends', 'earnings', 'pe_ratio', or 'news'."

#             return json.dumps(result, indent=4) if format == "json" else str(result)

#         except ValueError as e:
#             return f"ValueError: {str(e)}. Ensure ticker and parameters are correct."
#         except Exception as e:
#             return f"An error occurred: {str(e)}"

#     async def _arun(self, *args, **kwargs) -> str:
#         raise NotImplementedError("This tool does not support asynchronous execution.")

# # ------------------ Main Testing Function ------------------
# def main():
#     tool = FetchStockDataTool()

#     print("\nCurrent Stock Price (AAPL):")
#     print(tool._run(ticker="AAPL", data_type="current"))

#     print("\nHistorical Stock Data (AAPL, last 5 days):")
#     print(tool._run(ticker="AAPL", data_type="historical", start_date="2024-03-25", end_date="2024-03-30", format="json"))

#     print("\nCompany Info (AAPL):")
#     print(tool._run(ticker="AAPL", data_type="info", format="json"))

#     print("\nDividends Data (AAPL):")
#     print(tool._run(ticker="AAPL", data_type="dividends"))

#     print("\nEarnings Data (AAPL):")
#     print(tool._run(ticker="AAPL", data_type="earnings"))

#     print("\nP/E Ratio (AAPL):")
#     print(tool._run(ticker="AAPL", data_type="pe_ratio"))

#     print("\nSimulated News (AAPL):")
#     print(tool._run(ticker="AAPL", data_type="news", format="json"))

# # Run the test if this script is executed directly
# if __name__ == "__main__":
#     main()

import yfinance as yf
import json
from datetime import datetime
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class FetchStockDataInput(BaseModel):
    """Input schema for FetchStockDataTool."""
    ticker: str = Field(..., description="The stock ticker symbol (e.g., 'AAPL').")
    data_type: str = Field(
        "current",
        description="The type of data to fetch: 'current', 'historical', 'info', 'dividends', 'earnings', 'pe_ratio', or 'news'.",
    )
    start_date: str = Field(
        None,
        description="Start date for historical data (YYYY-MM-DD). Required if data_type is 'historical'."
    )
    end_date: str = Field(
        None,
        description="End date for historical data (YYYY-MM-DD). Required if data_type is 'historical'."
    )
    format: str = Field(
        "text",
        description="Output format: 'text' (default) or 'json'."
    )

class FetchStockDataTool(BaseTool):
    name: str = "Fetch Stock Data Tool"
    description: str = (
        "Fetches various types of stock data using the Yahoo Finance API, including current price, historical data, dividends, earnings, P/E ratio, and more."
    )
    args_schema: Type[BaseModel] = FetchStockDataInput

    def _run(self, ticker: str, data_type: str = "current", start_date: str = None, end_date: str = None, format: str = "text"):
        """Fetches stock data using yfinance and returns results in the requested format."""
        try:
            stock = yf.Ticker(ticker)
            result = {}

            # Fetch the requested data type
            if data_type == "current":
                history = stock.history(period="1d")
                if history.empty:
                    return f"No recent trading data available for {ticker}."
                current_price = history['Close'].iloc[-1]  # Fixed the warning by using `.iloc[-1]`
                result = {"ticker": ticker, "current_price": round(current_price, 2)}
            
            elif data_type == "historical":
                if not start_date or not end_date:
                    return "Start date and end date are required for historical data."
                
                historical_data = stock.history(start=start_date, end=end_date)
                if historical_data.empty:
                    return f"No historical data found for {ticker} from {start_date} to {end_date}."
                result = {"ticker": ticker, "historical_data": historical_data.to_dict()}

            elif data_type == "info":
                result = {"ticker": ticker, "info": stock.info or "No data available"}
            
            elif data_type == "dividends":
                dividends = stock.dividends
                result = {"ticker": ticker, "dividends": dividends.to_dict() if not dividends.empty else "No dividends data available."}
            
            elif data_type == "earnings":
                earnings = stock.earnings
                result = {"ticker": ticker, "earnings": earnings.to_dict() if not earnings.empty else "No earnings data available."}
            
            elif data_type == "pe_ratio":
                pe_ratio = stock.info.get("trailingPE", "N/A")
                result = {"ticker": ticker, "pe_ratio": pe_ratio}
            
            elif data_type == "news":
                news = [
                    {"title": f"Latest news for {ticker}", "date": datetime.now().isoformat(), "content": "Market news..."}
                ]
                result = {"ticker": ticker, "news": news}
            
            else:
                return f"Invalid data_type '{data_type}'. Options: 'current', 'historical', 'info', 'dividends', 'earnings', 'pe_ratio', or 'news'."
            
            # Format output
            if format == "json":
                return json.dumps(result, indent=4)
            elif format == "text":
                formatted_output = "\n".join([f"{key}: {value}" for key, value in result.items()])
                return formatted_output
            else:
                return f"Invalid format '{format}'. Options: 'text', 'json'."

        except ValueError as e:
            error_message = f"ValueError: {str(e)}. Ensure ticker and parameters are correct."
            print(error_message)
            return {"error": error_message}
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            print(error_message)
            return {"error": error_message}

# ------------------ Main Testing Function ------------------
if __name__ == "__main__":
    fetch_tool = FetchStockDataTool()

    print("\nCurrent Stock Price (AAPL):")
    print(fetch_tool._run(ticker="AAPL", data_type="current", format="text"))

    print("\nHistorical Stock Data (AAPL, last 5 days):")
    print(fetch_tool._run(ticker="AAPL", data_type="historical", start_date="2024-03-25", end_date="2024-03-30", format="json"))

    print("\nCompany Info (AAPL):")
    print(fetch_tool._run(ticker="AAPL", data_type="info", format="json"))

    print("\nDividends Data (AAPL):")
    print(fetch_tool._run(ticker="AAPL", data_type="dividends"))

    print("\nEarnings Data (AAPL):")
    print(fetch_tool._run(ticker="AAPL", data_type="earnings"))

    print("\nP/E Ratio (AAPL):")
    print(fetch_tool._run(ticker="AAPL", data_type="pe_ratio"))

    print("\nSimulated News (AAPL):")
    print(fetch_tool._run(ticker="AAPL", data_type="news", format="json"))
