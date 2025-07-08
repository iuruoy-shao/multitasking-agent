from crewai import Agent, Task, Crew, Process
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
class CodingAgents(Agent):
    """
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def manager(self) -> Agent:
        return BaseAgent(
            config = self.agents_config['manager'],
            verbose = True,
        )

    @agent
    def file_reader(self) -> Agent:
        return BaseAgent(
            config = self.agents_config['file_reader'],
            verbose = True,
            tools = [DirectoryReadTool(), FileReadTool()],
        )

    @agent
    def engineer(self) -> Agent:
        return BaseAgent(
            config = self.agents_config['engineer'],
            verbose = True,
            tools = [FileReadTool(), FileWriterTool(), MakeBranch(), Commit()],
        )

    @agent
    def git_manager(self) -> Agent:
        return BaseAgent(
            config = self.agents_config['git_manager'],
            verbose = True,
            # tools = ,
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

    @task
    def merge_pr(self) -> Task:
        return Task(
            config = self.tasks_config['merge_pr'],
            context = [], # Assuming context is an empty list based on tasks.yaml
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )