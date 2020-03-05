import os, sys
import discord
from functools import wraps
from inspect import signature

class Bot(discord.Client):

    # List of commands declared by @Bot.command decorator
    commands = {}

    def __init__(self, name, prefix=''):
        self.prefix = prefix
        self.name = name
        super().__init__()

    async def on_ready(self) -> None:
        """
        Discord event triggered on login

        :return: None
        """
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        print('Servers:')
        for g in self.guilds:
            print(g)
        print('------')

        object_methods = [method_name for method_name in dir(self) if callable(getattr(self, method_name))]
        for method in object_methods:
            try:
                if Bot.command in getattr(self, method)._decorators:
                    self.commands[method] = getattr(self, method)
            except AttributeError:
                continue

    async def on_message(self, msg: discord.Message) -> None:
        """
        Discord event triggered upon receipt of a message

        :param msg: Discord message received by the event
        :return: None
        """
        if self.prefix != '':
            if msg.author != self.user:
                if msg.content.startswith(self.prefix):
                    command = msg.content[1:].split(' ')[0]
                    args = msg.content[1:].split(' ')[1:]
                    await self.on_command(command, args, msg)

    def command(func: 'function') -> 'function':
        """
        Decorator to declare a command.
        Functions with this Decorator get their _decorators attribute
        set to (Bot.function,)

        :param func: Function for decorator input
        :return: Wrapped function
        """
        def wrapped(self, command, args, msg):
            return func(self, command, args, msg)

        wrapped._decorators = (Bot.command,)
        return wrapped

    async def on_command(self, command: str, args: list, msg: discord.Message) -> None:
        """
        Calls command functions

        :param command: The command that is being called
        :param args: Arguments that get passed to the command
        :param msg: The discord message sent by the user
        :return: None
        """
        if self.commands[command]:
            await self.commands[command](command, args, msg)

    def get_token(self, token_file: str = 'token') -> str:
        """
        Retrieves discord token from a token_file.
        Format: "<Bot.name> <token>"
        Example: "test_bot somecooltoken"

        :param token_file: Optional, path to token file relative to script
        :return: Token string
        """
        token = ''
        with open(self.path(token_file), 'r') as file:
            tokens = file.read().split('\n')
            for t in tokens:
                if self.name in t:
                    token = t.split(' ')[1]
        return token

    @staticmethod
    def path(filename: str) -> str:
        """
        Returns the absolute path to a file given by the relative path

        :param filename: Path to file relative to script
        :return: Absolute path to filename
        """
        path = os.path.dirname(sys.argv[0])
        if not path:
            path = '.'
        return path + '/' + filename
