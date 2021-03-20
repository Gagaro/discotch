import os
import queue
import threading

from discord_bot import client as discord_client
from twitch_bot import client as twitch_client


def run_discord_bot(from_discord_queue, from_twitch_queue):
    discord_client.run(
        os.getenv('DISCORD_TOKEN'),
        from_discord_queue=from_discord_queue,
        from_twitch_queue=from_twitch_queue,
    )


def run_twitch_bot(from_discord_queue, from_twitch_queue):
    twitch_client.run(from_discord_queue, from_twitch_queue)


if __name__ == '__main__':
    from_discord_queue = queue.SimpleQueue()
    from_twitch_queue = queue.SimpleQueue()

    discord_thread = threading.Thread(target=run_discord_bot, args=(from_discord_queue, from_twitch_queue))
    twitch_thread = threading.Thread(target=run_twitch_bot, args=(from_discord_queue, from_twitch_queue))

    discord_thread.start()
    twitch_thread.start()

    discord_thread.join()
    twitch_thread.join()
