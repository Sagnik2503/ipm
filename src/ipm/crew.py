from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from .models import (
    FinalReport,
    SerperNewsResponse,
    StockTrendAnalysisResult
)
from crewai_tools import EXASearchTool, ScrapeWebsiteTool
import json
from ipm.tools.serper_news import SerperNewsTool
from ipm.tools.serper2 import SerperNewsTool2
import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = LLM(
    model=os.getenv("MODEL"),
    api_key=GEMINI_API_KEY,
    temperature=0,
    streaming=True,
    stop=["###"]
)
 
knowledge=PDFKnowledgeSource(file_paths="project_manager_final_10_pages.pdf")

import json

# Define the file path
file_path = "/Users/sagniksengupta/Documents/CrewAI/ipm/output/project_overview.json"

# Read the JSON file and extract the project description


# Get project description

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Ipm():
    """Ipm crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher_agent'],
            verbose=True,
            llm=llm,
            embedder={
                "provider": "google",
                "config": {
                    "model": "models/text-embedding-004",
                    "api_key": GEMINI_API_KEY,
                }
            },
            knowledge_sources=[knowledge]
        )
    @agent
    def market_analysis_agent(self):
        exa_api_key = os.getenv('EXA_API_KEY')
        if not exa_api_key:
            raise ValueError("EXA_API_KEY environment variable is not set. Please check your environment variables.")
        return Agent(
            config=self.agents_config['market_analysis_agent'],
            verbose=True,
            # allow_delegation=True,
            llm=llm,
            tools=[SerperNewsTool(api_key=os.getenv('SERPER_API_KEY'))],
            
        )
    @agent
    def stock_analysis_agent(self):
        exa_api_key = os.getenv('EXA_API_KEY')
        if not exa_api_key:
            raise ValueError("EXA_API_KEY environment variable is not set. Please check your environment variables.")
        return Agent(
            config=self.agents_config['stock_analysis_agent'],
            verbose=True,
            llm=llm,
            tools=[EXASearchTool(api_key=exa_api_key), ScrapeWebsiteTool()]
            
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def document_query_task(self) -> Task:
        return Task(
            config=self.tasks_config['document_query_task'],
            output_pydantic=FinalReport,
            output_file="output/project_overview.json"
        )

    @task
    def market_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_analysis_task'],
            output_pydantic=SerperNewsResponse,
            output_file="output/market_analysis.json"
        )
        
    @task
    def stock_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['stock_analysis_task'],
            output_pydantic=StockTrendAnalysisResult,
            output_file="output/stock_analysis.json"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Ipm crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            knowledge_sources=[knowledge],
            embedder={
                "provider": "google",
                "config": {
                    "model": "models/text-embedding-004",
                    "api_key": GEMINI_API_KEY,
                }
            }
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
