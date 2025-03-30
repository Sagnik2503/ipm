from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict

class FinalReport(BaseModel):
    project_name: str
    client_name: str
    project_manager: str
    project_description: str  # A comprehensive description of the project
    objectives: List[str]  # List of specific objectives
    budget_overview: str  # Summary of budget details
    risks: List[str]  # List of identified risks
    mitigation_strategies: List[str]  # Corresponding strategies for the risks
    timeline: str  # Overview of the timeline
    key_phases: List[str]  # Important phases of the project
    conclusions: str  # Final remarks and conclusions about the project

class NewsArticle(BaseModel):
    """Represents a single news article from the Serper API response."""
    title: str = Field(..., description="Title of the news article")
    link: str = Field(..., description="URL to the full news article")
    snippet: Optional[str] = Field(None, description="Brief summary or snippet of the article")
    date: Optional[str] = Field(None, description="Publication date of the article")
    source: Optional[str] = Field(None, description="Name of the news source")
    imageUrl: Optional[str] = Field(None, description="URL of the thumbnail or featured image")

class SerperNewsResponse(BaseModel):
    """Represents the response from Serper API."""
    news: List[NewsArticle] = Field(..., description="List of news articles retrieved from Serper API")


class StockTrendAnalysisResult(BaseModel):
    stock_market_fluctuations: List[Dict[str, str]] = Field(
        ..., description="List of recent stock market fluctuations with details."
    )
    job_market_trends: List[Dict[str, str]] = Field(
        ..., description="Key job market trends affecting the stock market."
    )
    economic_news: List[Dict[str, str]] = Field(
        ..., description="Recent economic news impacting financial stability."
    )
    sector_performance: Dict[str, str] = Field(
        ..., description="Sector-wise performance summary."
    )
    investment_strategies: List[str] = Field(
        ..., description="Suggested investment strategies based on analysis."
    )