from src.crews.engineers.crew import Engineer
from src.crews.input_handler.crew import Manager, ValidationOutput
from src.crews.output_handler.crew import GitManager
from multiprocessing import Process, Queue
from termcolor import cprint
import git
import os

def launch_engineer(task: str, queue: Queue):
    cprint(f"✓ Task started: {task}", 'green')
    summary = Engineer().crew().kickoff(inputs={'task': task}).pydantic.response
    cprint(f"✓ Task completed: {task}, {summary.replace('\n', ' ')[:50]}...", 'green')
    queue.put(summary)
    
def git_init(directory: str):
    if not os.path.exists(f'{directory}/.git'): # creates a git repository if it doesn't exist
        repo = git.Repo.init(directory)
        repo.git.add(A=True)
        repo.index.commit('Initial commit')
        cprint(f"✓ Initialized git repository in {directory}", 'green')
    
    gitignore_path = f'{directory}/.gitignore'
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, 'r') as f:
            if '.temp' not in f.read():
                with open(gitignore_path, 'a') as f:
                    f.write('\n# Ignore temporary worktrees\n')
                    f.write('.temp\n')
    else:
        with open(gitignore_path, 'w') as f:
            f.write('# Ignore temporary worktrees\n')
            f.write('.temp\n')

def run(user_input: str, directory: str):
    os.chdir(directory)
    git_init(directory) # ensure git is initialized
    
    output = Manager().crew().kickoff(inputs={
        'user_input': user_input,
    }).pydantic

    cprint("✓ Validated user input", 'green')
    if isinstance(output, ValidationOutput):
        cprint(f"    ↳ {output.response}", 'grey')
        return

    cprint("✓ Parsed tasks", 'green')
    cprint(f"    ↳ Tasks: \n      - {'\n      - '.join(output.tasks)}", 'grey')

    queue = Queue()
    processes = [Process(target=launch_engineer, args=(task, queue)) for task in output.tasks]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
    
    cprint("✓ Merging changes", 'green')
    merges = GitManager().crew().kickoff(inputs={
        'tasks': output.tasks,
        'worktrees': os.listdir('.temp'),
    }).pydantic.merges

    for merge in merges:
        cprint(f"    ↳ Merged: '{merge.source_branch}' into '{merge.target_branch}'. {len(merge.conflicts)} conflicts resolved.", 'grey')