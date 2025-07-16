from crews.engineers.crew import Engineer
from crews.input_handler.crew import Manager, ValidationOutput
from crews.output_handler.crew import GitManager
from multiprocessing import Process, Queue
from termcolor import cprint
import git
import os

def launch_engineer(task: str, queue: Queue):
    cprint(f"✓ Task started: {task}", 'green')
    summary = Engineer().crew().kickoff(inputs={'task': task}).pydantic.response
    cprint(f"✓ Task completed: {task}, {summary.replace('\n', ' ')[:50]}...", 'green')
    queue.put(summary)

def run(user_input: str, directory: str):
    os.chdir(directory)

    # ensure repository is initialized
    if not os.path.exists(f'{directory}/.git'):
        repo = git.Repo.init(directory)
        repo.git.add(A=True)
        repo.index.commit('Initial commit')
        cprint(f"✓ Initialized git repository in {directory}", 'green')

    with open(f'{directory}/.gitignore', 'a+') as f:
        if '.temp' not in f.read():
            f.write('\n# Ignore temporary worktrees\n')
            f.write('.temp/\n')

    output = Manager().crew().kickoff(inputs={
        'user_input': user_input,
    }).pydantic

    cprint("✓ Validated user input", 'green')
    if isinstance(output, ValidationOutput):
        cprint(f"    ↳ {output.response}", 'grey')
        os.rmdir('.temp') # clean up
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