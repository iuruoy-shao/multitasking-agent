from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class GitManager():
    """
    """

    agents: List[BaseAgent]
    tasks: List[Task]
    
    @agent
    def git_manager(self) -> Agent:
        return BaseAgent(
            config = self.agents_config['git_manager'],
            verbose = True,
            # tools = ,
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
            verbose=True,
        )