from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
)
from crewai.tasks.conditional_task import ConditionalTask
from crewai.tasks.task_output import TaskOutput
from pydantic import BaseModel
from typing import List, Text

class ValidationOutput(BaseModel):
    valid: bool
    response: Text

class TaskList(BaseModel):
    tasks: List[Text]
    
def valid_input(output: TaskOutput) -> bool:
    return output.pydantic.valid

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
            output_pydantic = ValidationOutput,
        )
    
    @task
    def split_tasks(self) -> ConditionalTask:
        return ConditionalTask(
            config = self.tasks_config['split_tasks'],
            output_pydantic = TaskList,
            condition = valid_input,
        )    
    
    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )