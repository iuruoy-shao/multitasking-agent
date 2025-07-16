from main import run
from crewai import Task, Crew
from termcolor import colored
import cmd
import os

APP_NAME = "parallel-coding"

class CLI(cmd.Cmd):
    prompt = "✴ "
    
    def __init__(self):
        super().__init__()
        self.current_directory = None
            
    def do_setdir(self, arg):
        if os.path.exists(arg) and os.path.isdir(arg):
            self.current_directory = arg
            print(f"Current directory changed to {self.current_directory}")
        else:
            print(f"Directory '{arg}' does not exist.")
    
    def do_hey(self, arg):
        """Receive prompt"""
        if not self.current_directory:
            print("Please set the working directory first using 'setdir <path>'")
            return
        run(arg, self.current_directory)
    
    def do_quit(self, arg):
        """Exit the CLI."""
        print('Bye bye!')
        return True

    def do_exit(self, arg):
        return self.do_quit(arg)

if __name__ == "__main__":
    CLI().cmdloop()