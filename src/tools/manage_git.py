from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from git import Repo
from termcolor import cprint
from os import chdir
from subprocess import run, DEVNULL

class CommitArgs(BaseModel):
    commit_message: str = Field(description="The commit message. Should be short and descriptive of task completed.")

class BranchArgs(BaseModel):
    branch_name: str = Field(description="""The name of the worktree to create. 
                             Should describe the current task. 
                             No spaces, only dashes or underscores allowed. 
                             2-3 words ideal.""")

class MergeArgs(BaseModel):
    target_branch: str = Field(description="The name of the branch to merge into, corresponding to the contents of the folder with the same name in the .temp directory.")
    source_branch: str = Field(description="The name of the branch to merge from, corresponding to the contents of the folder with the same name in the .temp directory.")

class MakeWorktree(BaseTool):
    name: str = "Git Worktree Tool"
    description: str = "Creates a new worktree and branch in the repository. The worktree directory will be created in '.temp/{branch_name}'."
    args: Type[BaseModel] = BranchArgs

    def _run(self, branch_name: str) -> str:
        cprint(f"▶︎ Creating worktree: {branch_name}", 'magenta')
        try:
            run(["git", "worktree", "add", "--checkout", f".temp/{branch_name}"], stdout=DEVNULL, stderr=DEVNULL)
            chdir(f'.temp/{branch_name}')
            cprint("    ↳ Created worktree", 'green')
            return f"Successfully created and switched to worktree '{branch_name}'."
        except Exception as e:
            cprint("    ↳ Execution failed", 'red')
            return f"Error creating worktree: {e}"

class Commit(BaseTool):
    name: str = "Git Commit Tool"
    description: str = "Adds all changes and commits them onto the current branch."
    args: Type[BaseModel] = CommitArgs

    def _run(self, commit_message: str) -> str:
        cprint(f"▶︎ Committing changes: {commit_message}", 'magenta')
        try:
            repo = Repo('.')
            if not repo.index.diff(None) and not repo.untracked_files:
                return "No changes to commit."
            repo.git.add(A=True)
            repo.index.commit(commit_message)
            cprint(f"    ↳ Committed to branch '{repo.active_branch.name}'", 'green')
            return f"Successfully committed to branch '{repo.active_branch.name}' with message: '{commit_message}'"
        except Exception as e:
            cprint("    ↳ Execution failed", 'red')
            return f"Error making git commit: {e}"
        
class Merge(BaseTool):
    name: str = "Git Merge Tool"
    description: str = "Merges one branch into another."
    args: Type[BaseModel] = MergeArgs

    def _run(self, target_branch: str, source_branch: str) -> str:
        cprint(f"▶︎ Merging changes from {source_branch} into {target_branch}", 'magenta')
        try:
            repo = Repo('.')
            repo.git.checkout(target_branch)
            merge_response = run(["git", "merge", source_branch], capture_output=True).stdout.decode()
            git_status = run(["git", "status"], capture_output=True).stdout.decode()
            cprint(f"    ↳ Merged {source_branch} into {target_branch}: {merge_response.replace('\n', ' ')[:50]}...", 'green')
            return f"Began merging branch '{source_branch}' into '{target_branch}'. response from merge:{merge_response}. git status: {git_status}"
        except Exception as e:
            cprint(f"    ↳ Execution failed: {e}", 'red')
            return f"Error merging branches: {e}"