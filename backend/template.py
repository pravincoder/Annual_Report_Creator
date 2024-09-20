from crewai import Agent, Crew, Task
from crewai_tools import RagTool,TXTSearchTool
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from textwrap import dedent
load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant", stop_sequences=['\n', 'END'])

def template_maker():
    # Text Tool
    Text_tool = TXTSearchTool(
        config = dict(embedder= dict(provider="ollama", config=dict(model="all-minilm:latest")),
              vectordb=dict(provider="chroma", config=dict(collection_name='report_data',
                                                             dir='Report_data',
                                                             allow_reset=True)),        
        ),
        txt= './extracted_texts.txt'
    ) 

    # Agents
    Template_Agent = Agent(
        role = "Template Agent",
        goal = "Create a template for the report based on the extracted text",
        allow_delegation = False,
        backstory = ("The Template Agent is responsible for creating a template for the report based on the extracted text."),
        tools = [Text_tool],
        llm = llm
    )

    # Tasks 
    Template_task = Task(
        description = dedent(f"""
        Create a template for the report based on the extracted.
        # Things to consider:
             What information is important to include in the report?
             How should the information be organized?
             What sections and sub-sections should be included in the report?
             What should the layout of the report look like?
             How can the report be structured to make it easy to read and understand?
        # Make sure to take into account the following:
             The Template must be in markdown format.
             The Template must be easy to read and understand.
             The Template must be well-organized and structured.
        # Try To create a Mapping of the template at the end. 
            """),
        expected_output = dedent(f"""
            A template for the report based on the extracted text.
            Template must be in markdown format.
            Template must be have multiple sections and sub-sections.
            Template must have well-organized and structured layout.
        """),
        agent = [Template_Agent],    
    )

    # Crew 
    Template_Crew = Crew(
        tasks = [Template_task],
        agents=[Template_Agent],
        verbose = True,
        max_rpm=29
    )
    Created_template = Template_Crew.kickoff()
    return Created_template

if __name__ == "__main__":
    template = template_maker()
    print(template)