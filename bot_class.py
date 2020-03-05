import os, sys
import discord

class Bot(discord.Client):

    # List of commands declared by @Bot.command decorator
    commands = {}

    def __init__(self, name, prefix=''):
        # Prefix used for commands
        self.prefix = prefix
        # Name of the bot (relevant in the token file)
        self.name = name
        super().__init__()

    async def on_ready(self) -> None:
        """
        Discord event triggered on login
        Prints some information and loads commands

        :return: None
        """
        # Printing username and id of the bot
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        # Printing servers to which the bot was added
        if len(self.guilds) > 0:
            print('Servers:')
            for g in self.guilds:
                print('> ', g)
        else:
            print('Bot was not added to any servers yet.')
        print('------')

        self.get_command_functions()

    async def on_message(self, msg: discord.Message) -> None:
        """
        Discord event triggered upon receipt of a message
        Can be overridden if necessary

        :param msg: Discord message received by the event
        :return: None
        """
        # If the prefix is set
        if self.prefix != '':
            # Check if the received message was not sent by the bot itself
            if msg.author != self.user:
                if msg.content.startswith(self.prefix):
                    command = msg.content[1:].split(' ')[0]
                    args = msg.content[1:].split(' ')[1:]
                    # Send command with arguments to on_command function
                    await self.on_command(command, args, msg)

    def command(func: 'function') -> 'function':
        """
        Decorator to declare a command.
        Functions with this Decorator get their _decorators attribute
        set to (Bot.function,)

        :param func: Function for decorator input
        :return: Function with added _decorators attribute
        """
        func._decorators = (Bot.command,)
        return func

    async def on_command(self, command: str, args: list, msg: discord.Message) -> None:
        """
        Calls command functions

        :param command: The command that is being called
        :param args: Arguments that get passed to the command
        :param msg: The discord message sent by the user
        :return: None
        """
        # Check if command exists
        if self.commands[command]:
            # Call command function
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
            # Loop over all tokens in the file
            for t in tokens:
                # Check if name of token matches name of bot
                if self.name in t:
                    token = t.split(' ')[1]
        return token

    def get_command_functions(self) -> None:
        """
        Get the functions with an @Bot.command decorator and add them to the
        commands dict

        :return: None
        """
        # List of all methods of a bot object
        methods = [method for method in dir(self) if callable(getattr(self, method))]
        for method in methods:
            try:
                # Test if method has attribute _decorators
                if Bot.command in getattr(self, method)._decorators:
                    # Add command to commands list
                    self.commands[method] = getattr(self, method)
            except AttributeError:
                continue

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
