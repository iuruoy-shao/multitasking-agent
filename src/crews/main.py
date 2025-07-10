from engineers.crew import Engineer
from input_handler.crew import Manager
from output_handler.crew import GitManager

def run(user_input: str):
    Manager().crew().kickoff(inputs={
        'user_input': user_input,
        'dir': '/Users/Yourui/Documents/Caltech'
    })
    
if __name__ == "__main__":
    run("make a new, empty file called test.md in the a folder called test. also make a new file in the base directory called test2.md, this time with lipsum text")