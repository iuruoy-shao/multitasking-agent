from crewai import Agent, Task, Crew
from crewai.tools import BaseTool

agent = Agent(
    role="Coding Assistant",
    goal="Help users write high-quality code and solve programming problems",
    backstory="I am an AI coding assistant with expertise in multiple programming languages and software development best practices.",
    verbose=True,
    tools=[ShellCommandTool()],
    allow_delegation=False,
    llm=
)