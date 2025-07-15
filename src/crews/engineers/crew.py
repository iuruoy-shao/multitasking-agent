from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    FileWriterTool,
)
from src.tools.manage_git import MakeWorktree, Commit
from pydantic import BaseModel
from typing import List, Text

class EditOutput(BaseModel):
    response: Text

@CrewBase
class Engineer():
    """
    Completes user-given tasks via program edits.
    """

    agents: List[BaseAgent]
    tasks: List[Task]
    
    @agent
    def engineer(self) -> Agent:
        return Agent(
            config = self.agents_config['engineer'],
            verbose = True,
            tools = [DirectoryReadTool(), FileReadTool(), FileWriterTool(), MakeWorktree(), Commit()],
        )

    @task
    def make_changes(self) -> Task:
        return Task(
            config = self.tasks_config['make_changes'],
        )
        
    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )