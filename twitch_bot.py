import os
from queue import Empty

from discord.ext import tasks
from twitchbot import BaseBot, Message, channel


class DiscotchTwitchBot(BaseBot):
    def __init__(self, *args, **kwargs):
        self.channel = kwargs.pop('channel')
        super(DiscotchTwitchBot, self).__init__(*args, **kwargs)

    def run(self, from_discord_queue, from_twitch_queue):
        self.from_discord_queue = from_discord_queue
        self.from_twitch_queue = from_twitch_queue
        return super(DiscotchTwitchBot, self).run()

    async def on_privmsg_received(self, msg: Message):
        if msg.channel_name == self.channel:
            self.from_twitch_queue.put(f'{msg.author}: {msg.content}')


client = DiscotchTwitchBot(channel=os.getenv('TWITCH_CHANNEL'))


@tasks.loop(seconds=0.1)
async def send_message_from_discord():
    try:
        while True:
            message = client.from_discord_queue.get_nowait()
            await channel.channels[client.channel].send_message(message)
    except Empty:
        pass

send_message_from_discord.start()


if __name__ == '__main__':
    client.run(None, None)
