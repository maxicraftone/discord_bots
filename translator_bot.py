#!/usr/bin/python
import discord

class Translator_Client(discord.Client):
    prefix = '$'

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, msg):
        if msg.author != self.user:
            if msg.content.startswith(self.prefix):
                command = msg.content[1:].split(' ')[0]
                args = msg.content[1:].split(' ')[1:]
                if command == 'asciify':
                    await self.asciify(args)


    async def asciify(self, *args):
        print(args)


if __name__ == '__main__':
    token = ''
    with open('token', 'r') as token_file:
        token = token_file.read()[:-1]

    client = Translator_Client()
    client.run(token)
