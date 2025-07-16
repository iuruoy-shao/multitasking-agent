from engineers.crew import Engineer
from input_handler.crew import Manager, ValidationOutput
from output_handler.crew import GitManager
from multiprocessing import Process, Queue
import git
import os

def launch_engineer(task: str, queue: Queue):
    summary = Engineer().crew().kickoff(inputs={'task': task})
    queue.put(summary)

def run(user_input: str):
    directory = '/Users/Yourui/Documents/test'
    os.chdir(directory)
    
    # ensure repository is initialized
    if not os.path.exists(f'{directory}/.git'):
        repo = git.Repo.init(directory)
        repo.git.add(A=True)
        repo.index.commit('Initial commit')
        
    # add / modify .gitignore
    with open(f'{directory}/.gitignore', 'a') as f:
        f.write('\n# Ignore temporary worktrees\n')
        f.write('.temp/\n')

    output = Manager().crew().kickoff(inputs={
        'user_input': user_input,
    }).pydantic

    if isinstance(output, ValidationOutput):
        return output.response
    
    queue = Queue()
    processes = [Process(target=launch_engineer, args=(task, queue)) for task in output.tasks]

    for process in processes:
        process.start()

    summaries = [queue.get().pydantic.response for _ in processes]

    for process in processes:
        process.join()

    merge = GitManager().crew().kickoff(inputs={
        'tasks': summaries,
        'worktrees': os.listdir('.temp'),
    }).pydantic.merges
    
if __name__ == "__main__":
    run("add some lipsum to the beginning of test.txt. also add some lipsum to the end of test.txt")