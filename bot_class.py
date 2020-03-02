import os, sys
import discord

class Bot(discord.Client):
    def __init__(self, name, prefix=''):
        self.prefix = prefix
        self.name = name
        super().__init__()

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        print('Servers:')
        for g in self.guilds:
            print(g)
        print('------')

    async def on_message(self, msg):
        if prefix != '':
            if msg.author != self.user:
                if msg.content.startswith(self.prefix):
                    command = msg.content[1:].split(' ')[0]
                    args = msg.content[1:].split(' ')[1:]
                    self.on_command(command, args, msg)
    
    async def on_command(self, command, args, msg):
        pass

    def get_token(self, token_file='token'):
        token = ''
        with open(self.path('token'), 'r') as token_file:
            tokens = token_file.read().split('\n')
            for t in tokens:
                if self.name in t:
                    token = t.split(' ')[1]
        return token

    @staticmethod
    def path(filename):
        path = os.path.dirname(sys.argv[0])
        if not path:
            path = '.'
        return path + '/' + filename
