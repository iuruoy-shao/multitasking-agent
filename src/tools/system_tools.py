from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List
from termcolor import cprint
import subprocess
import os

class CommandArgs(BaseModel):
    command: List[str] = Field(..., description="The command to execute in the shell. This should be formatted as a list of strings, where each 'term' in the command is its own element, as commands are fed into subprocess.run(). For example, ['git', 'status'] in place of 'git status'.")
    
class DirectoryArgs(BaseModel):
    directory: str = Field(..., description="The directory to read. Should be a valid path relative to the current working directory.")

class Command(BaseTool):
    name: str = "Execute Command Tool"
    description: str = "This tool runs the given command, separated into a list of strings, in the shell. Can be used to check repository information, such as git status. DO NOT use this tool for purposes accomplishable with other tools (e.g. checking file paths, which can be completed via the Directory Read tool). "
    args: Type[BaseModel] = CommandArgs

    def _run(self, command: List[str]) -> str:
        cprint(f"▶︎ Running command: {' '.join(command)}", 'yellow')
        try:
            result = subprocess.run(command, capture_output=True)
            output = result.stdout.decode()
            if result.stderr:
                output += f"\nSTDERR:\n{result.stderr.decode()}"
            cprint(f"    ↳ Result: {output.replace('\n', ' ')[:50]}...", 'green')
            return output
        except Exception as e:
            cprint("    ↳ Execution failed", 'red')
            return f"Error executing command: {e}"
        
class DirectoryReadTool(BaseTool):
    name: str = "Directory Read Tool"
    description: str = "Reads the files and subdirectories in the specified path. This will only get the first level of child paths. If nothing is returned, the directory is empty."
    args: Type[BaseModel] = DirectoryArgs

    def _run(self, directory: str) -> str:
        cprint(f"▶︎ Reading Directory: {directory}", 'yellow')
        try:
            cprint("    ↳ Directories read", 'green')
            return os.listdir(directory)
        except Exception as e:
            cprint("    ↳ Execution failed", 'red')
            return f"Error reading directory: {e}"