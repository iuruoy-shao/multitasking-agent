from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from git import Repo
from os import system

class CommitArgs(BaseModel):
    commit_message: str = Field(..., description="The commit message. Should be short and descriptive of task completed.")

class BranchArgs(BaseModel):
    branch_name: str = Field(..., description="""The name of the worktree to create. 
                                                    Should describe the current task. 
                                                    No spaces, only dashes or underscores allowed. 
                                                    2-3 words ideal.""")

class MakeWorktree(BaseTool):
    name: str = "Git Worktree Tool"
    description: str = "Creates a new worktree and branch in the repository."
    args: Type[BaseModel] = BranchArgs

    def _run(self, branch_name: str) -> str:
        try:
            system(f"git worktree add --checkout '.temp/{branch_name}'")
            return f"Successfully created and switched to worktree '{branch_name}'."
        except Exception as e:
            return f"Error creating worktree: {e}"

class Commit(BaseTool):
    name: str = "Git Commit Tool"
    description: str = "Commits changes onto the current branch."
    args: Type[BaseModel] = CommitArgs

    def _run(self, commit_message: str) -> str:
        try:
            repo = Repo(search_parent_directories=True) # TODO: this probably causes problems
            if not repo.index.diff(None) and not repo.untracked_files:
                return "No changes to commit."
            repo.git.add(A=True)
            repo.index.commit(commit_message)
            return f"Successfully committed to branch '{repo.active_branch.name}' with message: '{commit_message}'"
        except Exception as e:
            return f"Error making git commit: {e}"