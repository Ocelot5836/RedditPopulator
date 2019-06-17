'''
Created on Jun 15, 2019

@author: Ocelot
'''

import json

import discord
import praw
import io
import aiohttp

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
		if(message.author.id == 117850765908770825):
			await message.channel.send('JACKSON HAS INFILTRATED THE SERVER! BURN ALL THE EVIDENCE!')
			return
		if(message.content.startswith('!help')):
			embed = discord.Embed(title='!help', description='Opens this menu', color=0xff00ff)
			embed.add_field(name="!populate", value="Posts a specified amount of Reddit posts into chat. Ex: !populate memes top 10", inline=False)
			await message.channel.send(embed=embed)
		if(message.content.startswith('!populate')):
			parts = message.content.split(' ')
			if len(parts) > 3:
				sub = reddit.subreddit(parts[1])
				if not parts[3].isdigit() or int(parts[3], 10) == 0 or int(parts[3], 10) > 25:
					await message.channel.send('Invalid Count')
					return
				if parts[2] == 'new':
					await message.channel.send('Posting ' + parts[3] + ' of the Newest Submissions from r/' + parts[1])
					submissions = sub.new(limit=int(parts[3], 10))
				elif parts[2] == 'top':
					await message.channel.send('Posting ' + parts[3] + ' of the Top Submissions from r/' + parts[1])
					submissions = sub.top(limit=int(parts[3], 10))
				else:
					await message.channel.send('Only new or top are accepted')
					return

				for submission in submissions:
					async with aiohttp.ClientSession() as session:
						async with session.get(submission.url) as resp:
							if resp.status != 200:
								return await channel.send('||' + submission.url + '||')
							data = io.BytesIO(await resp.read())
							await message.channel.send(file=discord.File(data, submission.url, spoiler=True))

			else:
				await message.channel.send('Not enough arguments.')

client = MyClient()
client.run(token)
