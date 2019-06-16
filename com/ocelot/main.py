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
            if len(parts) > 3:
                sub = reddit.subreddit(parts[1])
                if parts[2] == 'new':
                    await message.channel.send('Posting ' + parts[3] + ' of the Hottest Submissions from r/' + parts[1])
                    submissions = sub.new(limit=int(parts[3], 10))
                elif parts[2] == 'top':
                    await message.channel.send('Posting ' + parts[3] + ' of the Newest Submissions from r/' + parts[1])
                    submissions = sub.top(limit=int(parts[3], 10))
                else:
                    await message.channel.send('Only new or top are accepted')
                    return
                
                for submission in submissions:
                    await message.channel.send('||https://reddit.com' + submission.permalink + "||")
            else:
                await message.channel.send('Not enough arguments.')
            await message.delete()


client = MyClient()
client.run(token)
