from google.adk.agents import Agent
import subprocess

# import os

# HEADERS = {'Content-Type': 'application/json'}
# PARAMS = {'key': os.environ['GEMINI_API_KEY']}
# JSON_DATA = lambda text: {'contents': [{'parts': [{'text': text}]}]}

def write_to_cli(command: str) -> str:
    """Writes the given command to the user's shell and returns the output. 
    You can use this tool to access information (ex: file structures) about the user's system.
    
    Args:
        command (str): The command that will be executed in the user's shell.
    
    Returns:
        str: The resulting output of the command executed in the user's shell.
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)
    return result.stdout + result.stderr
    
agent = Agent(
    name="parallel_coding_agent",
    model="gemini-2.5-flash",
    description=(
        "Agent that will help write code."
    ),
    instruction=(
        f"""You are a coding assistant that helps users write code. 
        Before using any tool, explain what you are doing.
        """
    ),
    tools=[write_to_cli],
)