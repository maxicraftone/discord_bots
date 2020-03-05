#!/usr/bin/python
from bot_class import Bot

class ExampleBot(Bot):
    @Bot.command
    async def hello(self, command, args, msg):
        await msg.channel.send('Hiya')

if __name__ == '__main__':
    example_bot = TranslatorBot('example_bot', '$')
    example_bot.run(example_bot.get_token())
