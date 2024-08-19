from agent import Agent
from discordwrapper import DiscordWrapper
import time
import json
class AgentLoop:
    def __init__(self):
        self.discordWrapper = DiscordWrapper()
        self.agent = Agent(discordWrapper=self.discordWrapper)

    

    def run(self):
        self.agent.resetPrompt()
        while True:
            
            # check if new messages
            if not self.discordWrapper.checkForNewMessages():
                continue

            # set new message context every time
       
            self.discordWrapper.getMessagesInChannel()
            
              
            self.agent.resetPrompt()
 
            
            response = self.agent.generateResponse()
                
            if not response:
                raise Exception("No response from LLM")
                    
            if "}" not in response or "{" not in response:
                continue
                
            message = self.agent.parseAgentResponse(json.loads(response))
           
           
            self.discordWrapper.sendMessage(message)
            
            # remove this line if you don't want to wait in between sent messages
            time.sleep(1)


loop = AgentLoop()
loop.run()
