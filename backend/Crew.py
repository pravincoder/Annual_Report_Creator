from crewai import Agent, Crew, Process, Task
from crewai_tools import PDFSearchTool   # Might Switch to using RagTool for multiple file format support
from langchain_groq import ChatGroq
from textwrap import dedent
import os
from dotenv import load_dotenv
load_dotenv()
import yaml
llm=ChatGroq(model="llama-3.1-70b-versatile",api_key=os.getenv('GROQ_API_KEY'))

def report_crew(file_path:str)->str:
    # --- Tools ---
    pdf_search_tool = PDFSearchTool(
        name = "Report Data",
        description = "Extracting Data from different PDFs",
        config=dict(
            embedder=dict(provider="ollama", config=dict(model="all-minilm:latest")),
            llm=dict(provider="groq",config=dict(model="llama-3.1-70b-versatile",api_key=os.getenv('GROQ_API_KEY')))
        ),
        pdf=file_path,
    )

    # --- Agents ---
    report_research_agent = Agent(
        role=yaml.safe_load(open("config/agent.yaml"))["report_research_agent"]['role'],
        goal=yaml.safe_load(open("config/agent.yaml"))["report_research_agent"]['goal'],
        allow_delegation=False,
        verbose=True,
        backstory=yaml.safe_load(open("config/agent.yaml"))["report_research_agent"]['backstory'],
        tools=[pdf_search_tool],
        llm = llm
    )

    professional_writer_agent = Agent(
        role=yaml.safe_load(open("config/agent.yaml"))["professional_writer_agent"]['role'],
        goal=yaml.safe_load(open("config/agent.yaml"))["professional_writer_agent"]['goal'],
        allow_delegation=False,
        verbose=True,
        backstory=yaml.safe_load(open("config/agent.yaml"))["professional_writer_agent"]['backstory'],
        tools=[pdf_search_tool],
        llm = llm
    )

    # --- Tasks ---
    annual_report_task = Task(
        description=yaml.safe_load(open("config/task.yaml"))["writer_report_task"]['description'],
        expected_output=yaml.safe_load(open("config/task.yaml"))["writer_report_task"]['expected_output'],
        tools=[pdf_search_tool],
        agent=report_research_agent,
    )

    html_report_task = Task(
        description=yaml.safe_load(open("config/task.yaml"))["html_report_task"]['description'],
        expected_output=yaml.safe_load(open("config/task.yaml"))["html_report_task"]['expected_output'],
        tools=[],
        agent=professional_writer_agent,
    )

    # --- Crew ---
    crew = Crew(
        tasks=[annual_report_task, html_report_task],
        agents=[report_research_agent, professional_writer_agent],
        process=Process.sequential,
    )

    result = crew.kickoff()
    
    return result


