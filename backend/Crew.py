from crewai import Agent, Crew, Process, Task
from crewai_tools import PDFSearchTool,RagTool
from dotenv import load_dotenv

import os
from langchain_groq import ChatGroq
from textwrap import dedent
from flask import Flask, request, jsonify
load_dotenv()
from embedchain import App
llm=ChatGroq(model="llama-3.1-8b-instant",stop_sequences=['\n','END'])
app = App.from_config(config_path="config.yaml")

def report_crew(file_path:str):
    # --- Tools ---
    pdf_search_tool = PDFSearchTool(
        name = "Report Data",
        description = "Extracting Data from different PDFs",
        config=dict(
            embedder=dict(provider="ollama", config=dict(model="all-minilm:latest")),
        ),
        pdf=file_path,
    )


    # --- Agents ---
    report_research_agent = Agent(
        role="Annual Report Research Agent",
        goal="Search through the PDF to find relevant and important key events and information",
        allow_delegation=False,
        verbose=True,
        backstory=(
            """
            The Annual Report Research agent is adept at searching and 
            extracting data from documents, ensuring accurate and key informations.
            """
        ),
        tools=[pdf_search_tool],
        llm = llm
    )

    professional_writer_agent = Agent(
        role="Professional Annual Report Writer",
        goal="Write professional Report that have multiple sections in Markdown format and pages based on the research agent's findings and your own research",
        allow_delegation=False,
        verbose=True,
        backstory=(
            """
            The professional writer agent has excellent writing skills and is able to craft 
            clear and  based on the provided information.
            """
        ),
        tools=[],
        llm = llm
    )

    # --- Tasks ---
    annual_report_task = Task(
        description=dedent(
            f"""
            Create an Annual Report from the pdf provided .
            The report should be in markdown format and should have multiple sections,proper headings.
            Try to include as much relevant information as possible from the PDF.
            Some must include sections are: Page
            Here is the User Required Annual Report Template:
            
            """
        ),
        expected_output="""
            Provide clear and accurate annual report based on User Required Annual Report Template and 
            the content of the PDFs Data.
            """,
        tools=[pdf_search_tool],
        agent=report_research_agent,
    )

    markdown_report_task = Task(
        description=
            dedent(f"""
            Your Task is to create a Markdown Annual Report , based on the information provided by the research agent and tasks.
            You should make a report with Multiple Pages and sections.
            Here is the User Required Annual Report Template: 

            Here is a sample of some template you can use:-
            #Cover Page
            - Title of the Report
            - Name of Organization/Company or something similar(If applicable)
            - Year of the Report(If applicable)
                - page number :- 1
            #Table of Contents
            - List of all the sections and subsections with their page numbers
                - page number :- 2
            #Introduction(if applicable) 
                - Brief Introduction about the report
                    - page number :- according to the content
            # Executive Summary(if applicable)
                - Summary of the report
                    - page number :- according to the content
            # Chairperson's/CEO's Message(if applicable)
                - Message from the Chairperson/CEO
                    - page number :- according to the content
            #  Mission, Vision, and Values(if applicable)
                - Mission, Vision, and Values of the Organization
                    - page number :- according to the content
            #  Financial Highlights(if applicable)
                - Financial Highlights of the Organization
                    - page number :- according to the content
            #  Performance Highlights(if applicable)
                - Performance Highlights of the Organization
                    - page number :- according to the content
            #  Conclusion(if applicable)
                - Conclusion of the Report
                    - page number :- according to the content
            # References(if applicable)
                - References of the Report
                    - page number :- according to the content
            # Appendix(if applicable)
                - Appendix of the Report
                    - page number :- according to the content
            # Glossary(if applicable)
                - Glossary of the Report
                    - page number :- according to the content
            # Contact Information(if applicable)
                - Contact Information of the Organization
                    - page number :- according to the content 

        You can add and remove sections if you think it is necessary. Just make sure to include all the important information/events .

            """
        ),
        expected_output="""
            Write a clear and concise Annual Report of 7-15 pages , This report must ensure it effectively communicates all necessary information.
            """,
        tools=[],
        agent=professional_writer_agent,
    )

    # --- Crew ---
    crew = Crew(
        tasks=[annual_report_task, markdown_report_task],
        agents=[report_research_agent, professional_writer_agent],
        process=Process.sequential,
    )


    result = crew.kickoff()


