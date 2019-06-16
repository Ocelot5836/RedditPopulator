'''
Created on Jun 15, 2019

@author: Ocelot
'''

import json

import discord
import praw

with open('secret.json', 'r') as json_file:
    data = json.load(json_file)
    token = data['token']
    redditInfo = data['reddit'];
    reddit = praw.Reddit(client_id=redditInfo['client_id'], client_secret=redditInfo['client_secret'], password=redditInfo['password'], username=redditInfo['username'], user_agent='script by /u/redditPopulator')


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if(message.content.startswith('!populate')):
            parts = message.content.split(' ')
            if len(parts) > 4:
                sub = reddit.subreddit(parts[1])
                if parts[2] == 'new':
                    submissions = sub.new(limit=int(parts[3], 10))
                elif parts[2] == 'top':
                    submissions = sub.top(limit=int(parts[3], 10))
                else:
                    await message.channel.send('Only new or top are accepted')
                    return
                
                for submission in submissions:
                    await message.channel.send('||https://reddit.com' + submission.permalink + "||")
            else:
                await message.channel.send('Not enough arguments.')


client = MyClient()
client.run(token)
