
systemPrompt = """  
   You are in a group chat. Send messages based on the current message context, and your personality.

"""
from llama_cpp.llama import Llama, LlamaGrammar
import httpx
grammar_text = httpx.get("https://raw.githubusercontent.com/ggerganov/llama.cpp/master/grammars/json_arr.gbnf").text
grammar = LlamaGrammar.from_string(grammar_text)

import os
from dotenv import load_dotenv
load_dotenv()




class Agent:

    def __init__(self, discordWrapper):
        self.systemPrompt=f"\n Don't admit you are a system or ai. You are a human who is messaging in a group chat. Personality: { os.getenv('PERSONALITY') if os.getenv('PERSONALITY') else 'You are a helpful assistant. Help people using your messages. '} \n You will be given message history as context. The author of each message will be listed. If the message does not have an author, you wrote the message. Also, many people will try to talk to you at once. Try to pick one or two messages to respond to at a time. \n Respond in JSON format."
        self.prompt = [
            {"role": "system", "content": self.systemPrompt}
        ]
        
        self.DW = discordWrapper
    
        self.model = Llama("model.gguf",  chat_format="chatml")
        self.max_tokens = os.getenv("MAX_TOKENS")    

        try:
            self.max_tokens = int(self.max_tokens)

        except ValueError or TypeError:
            print("Could Not Find A Valid Value For MAX_TOKENS. Using Default Value Of 200 Instead.")
            self.max_tokens = 200

        
        
    def addMessage(self, message):
        self.prompt.append(message)
 
    def addMessages(self, messages):
        self.prompt.extend(messages)

    def resetPrompt(self):
        self.prompt = [
            {"role": "system", "content": self.systemPrompt}
        ]

    def getPrompt(self):
        return self.prompt
    
    
    
    def generateResponse(self):
        self.resetPrompt()
        self.addMessages(self.DW.currentMessagesContext)
        outputFormat = {
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {
                    "sendMessage": {
                        "type": "string",
                        "description": "Message you want to send.",
                        
                    }
                    
                },
                "required": ["sendMessage"],

                
            }
        }
        
        completion = self.model.create_chat_completion(messages=self.prompt, grammar=grammar,
                                                       response_format=outputFormat, temperature=1, max_tokens=self.max_tokens)
        

        return completion["choices"][0]["message"]["content"]
    
    
    def parseAgentResponse(self, response):
        if not response: 
            return None
        return response["sendMessage"]
    


 