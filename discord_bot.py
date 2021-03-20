import os
from queue import Empty

import discord
from discord.ext import tasks


class DiscotchDiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        self.channel_id = int(kwargs.pop('channel_id'))
        super(DiscotchDiscordClient, self).__init__(*args, **kwargs)

    def start(self, *args, **kwargs):
        self.from_discord_queue = kwargs.pop('from_discord_queue')
        self.from_twitch_queue = kwargs.pop('from_twitch_queue')
        return super(DiscotchDiscordClient, self).start(*args, **kwargs)


client = DiscotchDiscordClient(channel_id=os.getenv('DISCORD_CHANNEL_ID'))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    client.from_discord_queue.put(f'{message.author.name}: {message.content}')


@tasks.loop(seconds=0.1)
async def send_message_from_twitch():
    try:
        while True:
            message = client.from_twitch_queue.get_nowait()
            await client.get_channel(client.channel_id).send(message)
    except Empty:
        pass

send_message_from_twitch.start()


if __name__ == '__main__':
    client.run(os.getenv('DISCORD_TOKEN'))