from src.coding_agent.crew import create_coding_agent
from crewai import Task, Crew
from termcolor import colored
import cmd
import os
from typing import List

APP_NAME = "parallel-coding"

class CLI(cmd.Cmd):
    prompt = "✴ "
    
    def __init__(self):
        super().__init__()
        self.set_directory = False
        self.current_directory = os.getcwd()
        self.agent = create_coding_agent()
        self.crew = Crew(
            agents=[self.agent],
            tasks=[],
            verbose=True
        )
            
    def do_setdir(self, arg):
        new_dir = os.path.join(self.current_directory, arg)
        if os.path.exists(new_dir) and os.path.isdir(new_dir):
            self.current_directory = new_dir
            print(f"Current directory changed to {self.current_directory}")
        else:
            print(f"Directory '{arg}' does not exist.")
    
    def do_edit(self, arg):
        """Receive prompt"""
        print('prompt:', arg)
    
    def do_quit(self, arg):
        """Exit the CLI."""
        print('Bye bye!')
        return True

    def do_exit(self, arg):
        return self.do_quit(arg)
    
    def do_hey(self, input):
        if not input:
            print("Please provide a prompt.")
            return
            
        print(colored(f"Working on: {input}", 'blue'))
        
        task = Task(
            description=input,
            agent=self.agent,
            context=f"Current directory: {self.current_directory}"
        )
        
        self.crew.tasks = [task]
        result = self.crew.kickoff()
        
        print(colored("Response:", 'green', attrs=['bold']))
        print(result)

if __name__ == "__main__":
    CLI().cmdloop()