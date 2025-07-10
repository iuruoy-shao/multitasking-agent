from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from git import Repo

class CommitArgs(BaseModel):
    commit_message: str = Field(..., description="The commit message. Should be short and descriptive of task completed.")

class BranchArgs(BaseModel):
    branch_name: str = Field(..., description="""The name of the branch to create or switch to. 
                                                    Should describe the current task. 
                                                    No spaces, only dashes or underscores allowed. 
                                                    2-3 words ideal.""")

class MakeBranch(BaseTool):
    name: str = "Git Branch Tool"
    description: str = "Checks out a new branch in the current git repository."
    args: Type[BaseModel] = BranchArgs

    def _run(self, branch_name: str) -> str:
        try:
            repo = Repo(search_parent_directories=True)
            if branch_name in repo.branches:
                return f"Branch '{branch_name}' already exists."
            repo.git.checkout('-b', branch_name)
            return f"Successfully created and switched to branch '{branch_name}'."
        except Exception as e:
            return f"Error creating branch: {e}"

class Commit(BaseTool):
    name: str = "Git Commit Tool"
    description: str = "Commits changes onto the current branch."
    args: Type[BaseModel] = CommitArgs

    def _run(self, commit_message: str) -> str:
        try:
            repo = Repo(search_parent_directories=True)
            if not repo.index.diff(None) and not repo.untracked_files:
                return "No changes to commit."
            repo.git.add(A=True)
            repo.index.commit(commit_message)
            return f"Successfully committed to branch '{repo.active_branch.name}' with message: '{commit_message}'"
        except Exception as e:
            return f"Error making git commit: {e}"