import requests
import os
from dotenv import load_dotenv
load_dotenv()
import json

class DiscordWrapper:
    def __init__(self):
        self.headers = {
            "Authorization": os.getenv("DISCORD_TOKEN"),
            "Content-Type": "application/json",
        
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" ,
            
            }
        
        self.currentChannelID = os.getenv("CHANNEL_ID")
        self.lastMessageInChannel = None
        self.currentMessagesContext = []
        self.userID= os.getenv("USER_ID")
      
        if not self.userID: 
            raise ValueError("Need To Specify USER_ID In .env file!")
   
        if not self.currentChannelID:
            raise ValueError("Need To Specify CHANNEL_ID In .env file!")
    
    def getMessagesInChannel(self, returnEarly: bool = False ):
        if not self.currentChannelID:
            return []
           
     
        messages = requests.get(f"https://discord.com/api/v9/channels/{self.currentChannelID}/messages?limit=10", headers=self.headers)
    
        if not messages:
            print("request could not obtain messages")
            return []
            
        if returnEarly:
            return messages.json()
        
        self.formatMessages(messages.json())
        self.lastMessageInChannel = messages.json()[0]["id"]
       
    
    def formatMessages(self, messages: json):
        formattedMessages = []
        for item in messages:
            author = item["author"]["username"]
            authorID = item["author"]["id"]
            content = item["content"]

            if content == "":
                continue

            mes = {"role": "assistant" if authorID == self.userID else "user", "content":f"{author}: {content}" if authorID!= self.userID else content}

            formattedMessages.append(mes)
            
        # reverse so agent can see messages in order
        self.currentMessagesContext = formattedMessages[::-1]
            
    def checkForNewMessages(self):

        if not self.lastMessageInChannel:
            return True
        
        if not self.currentChannelID:
            return False
            
            
            
        newMessages = self.getMessagesInChannel(True)

        # no new message if last message in newMessages was by our agent
        if newMessages and newMessages[0]["author"]["id"] == self.userID:
            return False
            
        
        newMessagesLastMessageInChannel = newMessages[0]["id"]
        # no new message if last recorded last message is equal to the last message in the current channel messages
        if self.lastMessageInChannel == newMessagesLastMessageInChannel:
            return False

       

        return True
        
    def sendMessage(self, message: str) -> bool:
        if not self.currentChannelID:
            return False
        print("making request")
        response = requests.post(f"https://discord.com/api/v9/channels/{self.currentChannelID}/messages", headers=self.headers, data=json.dumps({"content": message}))

        if not response:
            return False
        
        return True
       