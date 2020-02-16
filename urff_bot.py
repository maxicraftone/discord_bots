#!/usr/bin/python
from bot_class import Bot

class UrffBot(Bot):
    async def on_message(self, msg):
        if msg.content.lower() == 'uff':
            await msg.channel.send('urff')

if __name__ == '__main__':
    urff_bot = UrffBot('urff_bot')
    urff_bot.run(urff_bot.get_token())
