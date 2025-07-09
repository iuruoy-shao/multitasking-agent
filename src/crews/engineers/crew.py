from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    FileWriterTool,
)
from tools.git import MakeBranch, Commit
from typing import List

@CrewBase
class Engineer():
    """
    """

    agents: List[BaseAgent]
    tasks: List[Task]
    
    @agent
    def engineer(self) -> Agent:
        return BaseAgent(
            config = self.agents_config['engineer'],
            verbose = True,
            tools = [DirectoryReadTool(), FileReadTool(), FileWriterTool(), MakeBranch(), Commit()],
        )
        
    @task
    def read_system(self) -> Task:
        return Task(
            config = self.tasks_config['read_system'],
            async_execution = True,
        )

    @task
    def make_changes(self) -> Task:
        return Task(
            config = self.tasks_config['make_changes'],
            context = [self.read_system()],
        )

    @task
    def create_branch(self) -> Task:
        return Task(
            config = self.tasks_config['create_branch'],
        )

    @task
    def commit_changes(self) -> Task:
        return Task(
            config = self.tasks_config['commit_changes'],
        )
        
    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )