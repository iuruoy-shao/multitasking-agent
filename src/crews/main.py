from engineers.crew import Engineer
from input_handler.crew import Manager, ValidationOutput
from output_handler.crew import GitManager
import git
import asyncio
import os

async def run(user_input: str):
    directory = '/Users/Yourui/Documents/test'
    os.chdir(directory) # ensure repository is initialized
    if not os.path.exists(f'{directory}/.git'):
        repo = git.Repo.init(directory)
        repo.git.add(A=True)
        repo.index.commit('Initial commit')

    output = Manager().crew().kickoff(inputs={
        'user_input': user_input,
    }).pydantic

    if isinstance(output, ValidationOutput):
        return output.response
    
    summaries = await Engineer().crew().kickoff_for_each_async([{ # TODO: check veracity of asyncness
        'task': task,
    } for task in output.tasks])
    
    for summary in summaries:
        print(summary.tasks_output)
    
    # kickoff_for_each_async()
    
if __name__ == "__main__":
    asyncio.run(run("make a new, empty file called test.md in a folder called 'hello_world'"))