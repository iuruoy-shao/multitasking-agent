from engineers.crew import Engineer
from input_handler.crew import Manager, TaskList
from output_handler.crew import GitManager
import asyncio

async def run(user_input: str):
    output = Manager().crew().kickoff(inputs={
        'user_input': user_input,
        'dir': '/Users/Yourui/Documents/test'
    }).pydantic
    
    if isinstance(output, TaskList): # If task splitting was completed, i.e., the user input was valid.
        await Engineer().crew().kickoff_for_each_async([{
            'task': task
        } for task in output.tasks])
    else:
        return output.response
    
    # kickoff_for_each_async()
    
if __name__ == "__main__":
    asyncio.run(run("make a new, empty file called test.md in a folder called 'hello_world'"))