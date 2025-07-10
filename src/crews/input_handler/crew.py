from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
)
from pydantic import BaseModel
from typing import List, Text

class TaskList(BaseModel):
    items: List[Text]

@CrewBase
class Manager():
    """
    Handling user input via task delegation.
    """
    
    agents: List[BaseAgent]
    tasks: List[Task]
    
    @agent
    def manager(self) -> Agent:
        return Agent(
            config = self.agents_config['manager'],
            verbose = True,
            tools = [DirectoryReadTool(), FileReadTool()],
        )
    
    @task
    def validate_response(self) -> Task:
        return Task(
            config = self.tasks_config['validate_response'],
        )
    
    @task
    def split_tasks(self) -> Task:
        return Task(
            config = self.tasks_config['split_tasks'],
            output_pydantic = TaskList,
        )    
    
    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )