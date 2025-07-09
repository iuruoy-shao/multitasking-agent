from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
)
from typing import List

@CrewBase
class Manager():
    """
    """
    
    agents: List[BaseAgent]
    tasks: List[Task]
    
    @agent
    def manager(self) -> Agent:
        return BaseAgent(
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
        )    
    
    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )