from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import (
    FileReadTool,
    FileWriterTool,
)
from src.tools.manage_git import Commit, Merge
from src.tools.system_tools import Command, DirectoryReadTool
from pydantic import BaseModel
from typing import List

class Conflict(BaseModel):
    source_version: str
    target_version: str
    merged_version: str

class MergeInfo(BaseModel):
    source_branch: str
    target_branch: str
    conflicts: List[Conflict]

class Merges(BaseModel):
    merges: List[MergeInfo]

@CrewBase
class GitManager():
    """
    Reviews git branches and appropriately merges them.
    """

    agents: List[BaseAgent]
    tasks: List[Task]
    
    @agent
    def git_manager(self) -> Agent:
        return Agent(
            config = self.agents_config['git_manager'],
            tools = [DirectoryReadTool(), FileReadTool(), FileWriterTool(), Commit(), Command(), Merge()],
        )
    
    @task
    def merge_changes(self) -> Task:
        return Task(
            config = self.tasks_config['merge_changes'],
            output_pydantic = Merges,
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )