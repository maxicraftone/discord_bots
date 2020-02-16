#!/usr/bin/python
from bot_class import Bot

class TranslatorBot(Bot):
    async def on_command(self, command, args, msg):
        if command == 'asciify':
            await self.asciify(args)

    async def asciify(self, args):
        pass

if __name__ == '__main__':
    translator_bot = TranslatorBot('translator_bot', '$')
    translator_bot.run(translator_bot.get_token())
