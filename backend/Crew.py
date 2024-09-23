from crewai import Agent, Crew, Process, Task
from crewai_tools import PDFSearchTool,RagTool

from langchain_groq import ChatGroq
from textwrap import dedent
from flask import Flask, request, jsonify

import os
llm=ChatGroq(model="llama-3.1-70b-versatile",api_key=os.getenv('GROQ_API_KEY'))

def report_crew(file_path:str)->str:
    # --- Tools ---
    pdf_search_tool = PDFSearchTool(
        name = "Report Data",
        description = "Extracting Data from different PDFs",
        config=dict(
            embedder=dict(provider="ollama", config=dict(model="all-minilm:latest")),
            llm=dict(provider="groq",config=dict(model="llama-3.1-70b-versatile",api_key=os.getenv('GROQ_API_KEY'))),),
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
        goal="Write professional Report that have multiple sections in HTML format and pages based on the research agent's findings and your own research",
        allow_delegation=False,
        verbose=True,
        backstory=(
            """
            The professional writer agent has excellent HTML coding skills and is able to craft 
            clear and professional report in html code based on the provided information.
            """
        ),
        tools=[pdf_search_tool],
        llm = llm
    )

    # --- Tasks ---
    annual_report_task = Task(
        description=dedent(
            f"""
        You are a Report data collector and Organizer , Your Task is to Search and Extract all the important information from the PDFs , so the 
        You should provide all the important information and key events from the PDFs in a structured format so that the Professional Writer can create a HTML based Annual Report.
        Try to make sections and include atleast 200 words in each section.
        The overall data should make atleast a 8-15 page report.  
            """
        ),
        expected_output="""
            Provide all the important information and key events from the PDFs in a structured format.
            Think about what information would be important to include in an Annual Report and Different Sections and Subsections..
            """,
        tools=[pdf_search_tool],
        agent=report_research_agent,
    )

    HTML_report_task = Task(
        description=
            dedent(f"""
        You are a Professional Coder of Frontend with skills in HTML and CSS , Your Task is to Create a Professional Annual Report in HTML format based on the information provided by the Research Agent and previous task.
        The Report should have multiple sections and subsections based on the key events and information provided make sure to include atleast 200 words in each section.
        The Report should have atleast 8-15 pages.
        Make every page look professional and readable.
        Make sure to include a Table of Contents, Page Numbering and Footer.
        Text should be of Big Font and Readable.
        
            Here is a sample of some template you can use:-
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Report Title</title>
            <style>
            Create CSS Style for the following:
            - Use h1,h2,h3 ,p tags Depending on the Title ,Section,subsections and paragraphs 
            -Font Selection ,Color Selection , based on tags and sections
            -Page Numbering and Footer
            -Highlighting Important Information if possible 
            </style>
        </head>
        <body>

            <div class="cover-page">
                <h1>Title of the Report</h1>
                <p><strong>Name of Organization/Company:</strong> [Insert Name]</p>
                <p><strong>Year of the Report:</strong> [Insert Year]</p>
                <div class="page-number">Page 1</div>
            </div>

            <div class="table-of-contents">
                <h2>Table of Contents</h2>
                <ul>
                    <li><a href="#introduction">Introduction</a> - Page 2</li>
                    <li><a href="#executive-summary">Executive Summary</a> - Page 3</li>
                    <li><a href="#ceo-message">Chairperson's/CEO's Message</a> - Page 4</li>
                    <li><a href="#mission-vision-values">Mission, Vision, and Values</a> - Page 5</li>
                    <li><a href="#financial-highlights">Financial Highlights</a> - Page 6</li>
                    <li><a href="#performance-highlights">Performance Highlights</a> - Page 7</li>
                    <li><a href="#conclusion">Conclusion</a> - Page 8</li>
                    <li><a href="#glossary">Glossary</a> - Page 9</li>
                    <li><a href="#contact-info">Contact Information</a> - Page 10</li>
                </ul>
                <div class="page-number">Page 2</div>
            </div>

            <div class="section" id="introduction">
                <h2>Introduction</h2>
                <p>Brief Introduction about the report.</p>
                <div class="page-number">Page 3</div>
            </div>

            <div class="section" id="executive-summary">
                <h2>Executive Summary</h2>
                <p>Summary of the report.</p>
                <div class="page-number">Page 4</div>
            </div>

            <div class="section" id="ceo-message">
                <h2>Chairperson's/CEO's Message</h2>
                <p>Message from the Chairperson/CEO.</p>
                <div class="page-number">Page 5</div>
            </div>

            <div class="section" id="mission-vision-values">
                <h2>Mission, Vision, and Values</h2>
                <p>Mission, Vision, and Values of the Organization.</p>
                <div class="page-number">Page 6</div>
            </div>

            <div class="section" id="financial-highlights">
                <h2>Financial Highlights</h2>
                <p>Financial Highlights of the Organization.</p>
                <div class="page-number">Page 7</div>
            </div>

            <div class="section" id="performance-highlights">
                <h2>Performance Highlights</h2>
                <p>Performance Highlights of the Organization.</p>
                <div class="page-number">Page 8</div>
            </div>

            <div class="section" id="conclusion">
                <h2>Conclusion</h2>
                <p>Conclusion of the Report.</p>
                <div class="page-number">Page 9</div>
            </div>

            <div class="section" id="glossary">
                <h2>Glossary</h2>
                <p>Glossary of the Report.</p>
                <div class="page-number">Page 10</div>
            </div>

            <div class="section" id="contact-info">
                <h2>Contact Information</h2>
                <p>Contact Information of the Organization.</p>
                <div class="page-number">Page 11</div>
            </div>

        </body>
        </html>


        You can add and remove sections if you think it is necessary. Just make sure to include all the important information/events .
        You can use Different CSS Styles,Fonts,Colors to make it look professional and Readable.
        If you HTML Coded Report is Loved by the User, you will be Rewarded with a Bonus.
            """
        ),
        expected_output="""
            Write a clear and concise Annual Report of 7-15 pages , This report must ensure it effectively communicates all necessary information.
            The Final Output should be the entire Report in HTML Code.
            """,
        tools=[],
        agent=professional_writer_agent,
    )

    # --- Crew ---
    crew = Crew(
        tasks=[annual_report_task, HTML_report_task],
        agents=[report_research_agent, professional_writer_agent],
        process=Process.sequential,
    )

    result = crew.kickoff()
    
    return result

if __name__ == "__main__":
    report_crew("merged_document.pdf")

