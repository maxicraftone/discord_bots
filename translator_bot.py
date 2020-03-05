#!/usr/bin/python
from bot_class import Bot

class TranslatorBot(Bot):
    @Bot.command
    async def asciify(self, command, args, msg):
        await msg.channel.send('Not ready yet')

    @Bot.command
    async def some_func(self):
        pass

if __name__ == '__main__':
    translator_bot = TranslatorBot('translator_bot', '$')
    translator_bot.run(translator_bot.get_token())
