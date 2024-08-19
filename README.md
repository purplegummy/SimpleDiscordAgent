# SimpleDiscordAgent
This is for educational purposes only! Don't actually use this 😉


Here is step by step process on how to use the agent. For this repo, this will be running locally, so your computer should be able to load and run a model in order for this to work. 

First clone this github repo and ensure you have a modern version of python installed. 

Second, obtain the authentication token of the discord account you would like the agent to run on. In order to do this, first go to discord.com, and login to the account on the browser. Once you are there, open dev tools. You can do this by pressing CTRL + SHIFT + C. You should see something like this: 
![image](https://github.com/user-attachments/assets/560b4a87-1d9c-4070-98e7-75dea2cabd07)

Click on network as shown in the image. Next click on Fetch/XHR to filter the requests. 

![image](https://github.com/user-attachments/assets/41157a43-37b1-49ee-8d14-380a05ce8955)

Then refresh your page. 

Look for a request that says @me and click it. 

![image](https://github.com/user-attachments/assets/a21887e1-482c-456c-8943-08dd0108f397)

Click on headers, and then copy the value next to "Authorization: "

Place this value in the .env for in between the quotes for DISCORD_TOKEN. 

Next you want to enable developer mode in discord (on another account, probably your main account) to obtain user ids and channel ids. Here is a tutorial on how to do that: https://www.howtogeek.com/714348/how-to-enable-or-disable-developer-mode-on-discord/

Then, add the agent discord account as a friend.

Once you have added the account as a friend, on your main account, right click the profile of your alternate account.
![image](https://github.com/user-attachments/assets/c5630831-809a-4102-9698-c3ebb8953ac3)

Click on copy user id, and paste that into the .env for USER_ID.

Then you want to find a channel you would like the agent to type in. Right click on the channel, and copy channel id. Put this value in for CHANNEL_ID in the .env file.

If you would like, you an alter the personality for the agent in the .env file as well.

After you have finished adding the values to the env file, run ``pip install -r requirements.txt`` in a terminal in the same directory as the project.

Then, find a large language model on https://huggingface.co/ and install the .gguf. Move this file into the project directory and rename it to model.gguf 

Finally, just run ``main.py`` and the agent should start typing once a message has been detected. 


