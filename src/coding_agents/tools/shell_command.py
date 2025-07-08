import subprocess
from crewai.tools import BaseTool

class ShellCommand(BaseTool):
    name: str = "Shell Command"
    description: str = "Execute shell commands to access information about the user's system"
    
    def _run(self, command: str) -> str:
        """Executes a shell command and returns the output.
        Args:
            command (str): The command to execute in the user's shell.
        Returns:
            str: The combined stdout and stderr from the command execution.
        """
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)
        return result.stdout + result.stderr