'''
Created on Jun 15, 2019

@author: Ocelot
'''

import json
import discord

with open('secret.json', 'r') as json_file:
    data = json.load(json_file)
    token = data['token']

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.content.startswith('!deleteme'):
            msg = await message.channel.send('I will delete myself now...')
            await msg.delete()

            # this also works
            await message.channel.send('Goodbye in 3 seconds...', delete_after=3.0)

    async def on_message_delete(self, message):
        fmt = '{0.author.mention} has deleted the message: {0.content}'
        await message.channel.send(fmt.format(message))

client = MyClient()
client.run(token)