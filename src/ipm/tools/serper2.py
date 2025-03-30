import requests
import json
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field, PrivateAttr
import os

class SerperNewsToolInput(BaseModel):
    """Input schema for Serper News Tool."""
    query: str = Field(
        description="A brief or overview of the project or market interest area."
    )

class SerperNewsTool2(BaseTool):
    name: str = "Serper Market News Tool"
    description: str=(
        "Fetches the latest market-related news articles relevant to the specified query using the Serper API."
    )
    args_schema: Type[BaseModel] = SerperNewsToolInput
    _api_key: str = PrivateAttr()  # Private attribute for the API key

    def __init__(self, api_key: str = None):
        """
        Initialize the tool with an API key.
        If no key is provided, it attempts to read from the environment variable.
        """
        super().__init__()
        self._api_key = api_key or os.getenv('SERPER_API_KEY')
        if not self._api_key:
            raise ValueError("Serper API key is required. Set SERPER_API_KEY environment variable.")

    def _run(self, query: str):
        """Fetch and filter market-relevant news articles."""
        gl = "in"   # Country code (India)
        tbs = "qdr:w"  # Time range (last week)

        url = "https://google.serper.dev/news"
        payload = json.dumps({
            "q": query,
            "gl": gl,
            "tbs": tbs,
            "num": 15
        })
        headers = {
            'X-API-KEY': self._api_key,
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)

        # Handle response errors
        if response.status_code != 200:
            error_message = {
                "error": f"Received {response.status_code} from API",
                "details": response.text
            }
            print(json.dumps(error_message, indent=2))  # Print error in JSON format
            return error_message

        data = response.json()
        news_articles = data.get("news", [])

        # Define market-related keywords
        market_keywords = [
            "stock market", "financial trends", "investment", "economy", "market analysis",
            "industry growth", "business strategy", "market research", "trading", "business news"
        ]

        # Filter articles for market relevance
        filtered_articles = [
            article for article in news_articles
            if any(keyword in article.get('snippet', '').lower() or keyword in article.get('title', '').lower()
                   for keyword in market_keywords)
        ]

        if not filtered_articles:
            print("No market-related news articles found.")
            return {"message": "No market-related news articles found."}

        # Format and print filtered articles
        formatted_results = []
        for article in filtered_articles:
            formatted_article = (
                f"📌 *{article['title']}*\n"
                f"🔗 [Read More]({article['link']})\n"
                f"🗞 Source: {article['source']} | 📅 Date: {article['date']}\n"
                f"📝 {article['snippet']}\n"
            )
            formatted_results.append(formatted_article)

        print("\n\n".join(formatted_results))  # Print the articles

        return filtered_articles  # Return the filtered articles

# Run the tool
if __name__ == "__main__":
    news_tool = SerperNewsTool2(api_key=os.getenv('SERPER_API_KEY'))
    news_results = news_tool._run(query="market trends and financial news")

    print("\n\nReturned JSON Object:\n", news_results)  # Print returned JSON separately
    print("\nType of returned data:", type(news_results))