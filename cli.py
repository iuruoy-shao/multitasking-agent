from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import agent
from termcolor import colored
import cmd
import os

APP_NAME = "parallel-coding"
USER_ID = "user"
SESSION_ID = "session"

tool_call_formatting = {
    'write_to_cli': lambda function_call: colored(function_call.args['command'], 'cyan', attrs=['bold'])
}
tool_response_formatting = {
    'write_to_cli': lambda function_response: colored(function_response.response['result'], 'green', attrs=['bold'])
}
    

def format_event(event):
    response = []
    for part in event.content.parts:
        if part.text:
            response.append(part.text)
        if part.function_call:
            response.append(tool_call_formatting[part.function_call.name](part.function_call))
        if part.function_response:
            response.append(tool_response_formatting[part.function_response.name](part.function_response))
    return response

class CLI(cmd.Cmd):
    prompt = "✴ "
    
    # Add code to set up Gemini API key
    
    def __init__(self):
        super().__init__()
        self.set_directory = False
        self.current_directory = os.getcwd()
        session_service = InMemorySessionService()
        session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
        self.runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)
            
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
        content = types.Content(role='user', parts=[types.Part(text=input)])
        events = self.runner.run(new_message=content, user_id=USER_ID, session_id=SESSION_ID)

        for event in events:
            if event.is_final_response():
                print(event.content.parts)
    
# CLI().cmdloop()
input = "what files do i have in this directory?"
session_service = InMemorySessionService()
session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)
        
content = types.Content(role='user', parts=[types.Part(text=input)])
events = runner.run(new_message=content, user_id=USER_ID, session_id=SESSION_ID)

for event in events:
    print(*format_event(event))