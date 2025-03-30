import requests
import json
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field, PrivateAttr
import os

class SerperNewsToolInput(BaseModel):
    """Input schema for Serper News Tool."""
    query: str = Field(
        description="A brief or overview of the project"
    )

class SerperNewsTool(BaseTool):
    name: str = "Serper News Extraction Tool"
    description: str = (
        "Retrieves the most recent and relevant news articles related to the project description using the Serper API."
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
        """Fetch news articles using the Serper API and return JSON data."""
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

        # Format and print news articles
        if not news_articles:
            print("No news articles found.")
        else:
            formatted_results = []
            for article in news_articles:
                formatted_article = (
                    f"📌 **{article['title']}**\n"
                    f"🔗 [Read More]({article['link']})\n"
                    f"🗞 Source: {article['source']} | 📅 Date: {article['date']}\n"
                    f"📝 {article['snippet']}\n"
                )
                formatted_results.append(formatted_article)

            # Print formatted results
            print("\n\n".join(formatted_results))

        return news_articles  # Return raw JSON data

# Run the tool
if __name__ == "__main__":
    news_tool = SerperNewsTool(api_key=os.getenv('SERPER_API_KEY'))
    news_results = news_tool._run(query="AI Agents")

    print("\n\nReturned JSON Object:\n", news_results)  # Print returned JSON separately
    print("\nType of returned data:", type(news_results))

# import requests
# import json
# import os
# from crewai.tools import BaseTool
# from typing import Type
# from pydantic import BaseModel, Field, PrivateAttr

# class SerperNewsToolInput(BaseModel):
#     """Input schema for Serper News Tool."""
#     query: str = Field(description="A brief or overview of the project.")

# class SerperNewsTool(BaseTool):
#     name: str = "Serper News Extraction Tool"
#     description: str = (
#         "Retrieves the most recent and relevant news articles related to the project description using the Serper API."
#     )
#     args_schema: Type[BaseModel] = SerperNewsToolInput
#     _api_key: str = PrivateAttr()
#     _query: str = PrivateAttr()

#     def __init__(self, query: str, api_key: str = None):
#         """
#         Initialize the tool with an API key and query.
#         """
#         super().__init__()
#         self._api_key = api_key or os.getenv('SERPER_API_KEY')
#         self._query = query  # Store query as an instance variable

#         if not self._api_key:
#             raise ValueError("Serper API key is required. Set SERPER_API_KEY environment variable.")

#     def _run(self):
#         """Fetch news articles using the Serper API and return JSON data."""
#         gl = "in"   # Country code (India)
#         tbs = "qdr:w"  # Time range (last week)

#         url = "https://google.serper.dev/news"
#         payload = json.dumps({
#             "q": self._query,  # Use the instance's query attribute
#             "gl": gl,
#             "tbs": tbs,
#             "num": 20
#         })
#         headers = {
#             'X-API-KEY': self._api_key,
#             'Content-Type': 'application/json'
#         }

#         response = requests.post(url, headers=headers, data=payload)

#         if response.status_code != 200:
#             error_message = {
#                 "error": f"Received {response.status_code} from API",
#                 "details": response.text
#             }
#             print(json.dumps(error_message, indent=2))
#             return error_message

#         data = response.json()
#         news_articles = data.get("news", [])

#         if not news_articles:
#             print("No news articles found.")
#             return []

#         formatted_results = []
#         for article in news_articles:
#             formatted_article = (
#                 f"📌 **{article['title']}**\n"
#                 f"🔗 [Read More]({article['link']})\n"
#                 f"🗞 Source: {article['source']} | 📅 Date: {article['date']}\n"
#                 f"📝 {article['snippet']}\n"
#             )
#             formatted_results.append(formatted_article)

#         print("\n\n".join(formatted_results))
#         return news_articles  # Return raw JSON data

# # Example usage
# if __name__ == "__main__":
#     query_text = "AI in business automation"  # Example query
#     news_tool = SerperNewsTool(query=query_text, api_key=os.getenv('SERPER_API_KEY'))
#     news_results = news_tool._run()

#     print("\n\nReturned JSON Object:\n", news_results)
#     print("\nType of returned data:", type(news_results))
