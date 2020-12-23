#!/usr/bin/python
from bot_class import Bot
import discord

users = {'max': 349624423709671426, 'luca': 459954558131503106}

class CallBot(Bot):
    def __init__(self, name, prefix, mode='command'):
        """
        Mode can be 'command' or 'file'
        """
        self.mode = mode
        super().__init__(name, prefix)

    async def on_ready(self):
        await super().on_ready()
        if self.mode == 'file':
            while True:
                with open('calls.txt', 'r') as calls_file:
                    content = calls_file.read()
                    if len(content) > 0:
                        calls = [i for i in content.split('\n') if i != '']
                        for call in calls:
                            call = call.split(' ')
                            if call[0] == 'textall':
                                for user in ['max']:
                                    await self.send_text(user, call[1])
                with open('calls.txt', 'w') as calls_file:
                    calls_file.write('')

    @Bot.command
    async def textall(self, command, args, msg):
        if self.mode == 'command':
            if msg.author.id == users['max']:
                await self.send_text('max', args[0])

    async def send_text(self, receiver: str, text: str):
        user = await self.fetch_user(users[receiver])
        await user.send(text)

    @Bot.command
    async def myid(self, command, args, msg):
        await msg.channel.send(msg.author.id)

if __name__ == '__main__':
    call_bot = CallBot('mx_bot', '!', 'file')
    call_bot.run(call_bot.get_token())
