from engineers.crew import Engineer
from input_handler.crew import Manager
from output_handler.crew import GitManager

def run(user_input: str):
    task_list = Manager().crew().kickoff(inputs={
        'user_input': user_input,
        'dir': '/Users/Yourui/Documents/Caltech'
    })
    print(task_list)
    
if __name__ == "__main__":
    run("what files are in my directory?")