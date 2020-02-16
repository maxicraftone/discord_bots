#!/usr/bin/python
from bot_class import Bot

class UrffBot(Bot):
    async def on_message(self, msg):
        if 'uff' in msg.content.lower() or 'oof' in msg.content.lower():
            await msg.channel.send('URFF')

if __name__ == '__main__':
    urff_bot = UrffBot('urff_bot')
    urff_bot.run(urff_bot.get_token())
