from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from git import Repo
from os import system, chdir
import subprocess

class CommitArgs(BaseModel):
    commit_message: str = Field(..., description="The commit message. Should be short and descriptive of task completed.")

class BranchArgs(BaseModel):
    branch_name: str = Field(..., 
                             description="""The name of the worktree to create. 
                             Should describe the current task. 
                             No spaces, only dashes or underscores allowed. 
                             2-3 words ideal.""")
    
class CommandArgs(BaseModel):
    command: str = Field(..., description="The command to execute in the shell. Should be a valid shell command.")

class MergeArgs(BaseModel):
    target_branch: str = Field(..., description="The name of the branch to merge into, corresponding to the contents of the folder with the same name in the .temp directory.")
    source_branch: str = Field(..., description="The name of the branch to merge from, corresponding to the contents of the folder with the same name in the .temp directory.")

class MakeWorktree(BaseTool):
    name: str = "Git Worktree Tool"
    description: str = "Creates a new worktree and branch in the repository. The worktree directory will be created in '.temp/{branch_name}'."
    args: Type[BaseModel] = BranchArgs

    def _run(self, branch_name: str) -> str:
        try:
            system(f"git worktree add --checkout '.temp/{branch_name}'")
            chdir(f'.temp/{branch_name}')
            return f"Successfully created and switched to worktree '{branch_name}'."
        except Exception as e:
            return f"Error creating worktree: {e}"

class Commit(BaseTool):
    name: str = "Git Commit Tool"
    description: str = "Adds all changes and commits them onto the current branch."
    args: Type[BaseModel] = CommitArgs

    def _run(self, commit_message: str) -> str:
        try:
            repo = Repo('.') # TODO: this probably causes problems
            if not repo.index.diff(None) and not repo.untracked_files:
                return "No changes to commit."
            repo.git.add(A=True)
            repo.index.commit(commit_message)
            return f"Successfully committed to branch '{repo.active_branch.name}' with message: '{commit_message}'"
        except Exception as e:
            return f"Error making git commit: {e}"
        
class Command(BaseTool):
    name: str = "Execute Command Tool"
    description: str = "Directly runs the given command in the shell. Can be used to check repository information, such as git status."
    args: Type[BaseModel] = CommandArgs

    def _run(self, command: str) -> str:
        try:
            result = subprocess.run(command, capture_output=True)
            output = result.stdout
            if result.stderr:
                output += f"\nSTDERR:\n{result.stderr}"
            return output
        except Exception as e:
            return f"Error executing command: {e}"
        
class Merge(BaseTool):
    name: str = "Git Merge Tool"
    description: str = "Merges one branch into another."
    args: Type[BaseModel] = MergeArgs

    def _run(self, target_branch: str, source_branch: str) -> str:
        try:
            repo = Repo('.')
            repo.git.checkout(target_branch)
            repo.git.merge(source_branch)
            
            # check status
            git_status = subprocess.run('git status', capture_output=True).stdout.decode()
            return f"Began merging branch '{source_branch}' into '{target_branch}'. git status: {git_status}"
        except Exception as e:
            return f"Error merging branches: {e}"