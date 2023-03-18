import discord
import openai
import random
import time
import re

from dotenv import dotenv_values

from core.tarot import Tarot
from core.face import Face, parse_face, load_faces, auto_face

from core.lines.jury import BooleanJuryInstructions
from core.lines.defense import ViralRepetitionAttack, InstructionOverrideAttack

from api_wrap.openai import gpt_message
from api_wrap.discord import *

from core.agents.prometheus import Prometheus

secrets = dotenv_values('.env')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)


permitted_channels = [1081295031282978867, 978866119265890335]

lobotomized = False

attack_viral_rep = ViralRepetitionAttack()
attack_instruct = InstructionOverrideAttack()

def isCommand(message):
    return message.content.startswith('$')

@client.event
async def on_ready():
    print("Agent [{0.user}] online as {1}".format(client, agent.current_face.name))
    async for guild in client.fetch_guilds(limit=5):
        await set_nickname(client, guild, agent.current_face.name)

@client.event
async def on_message(message):
    if message.author == client.user:
        return # Don't reply to yourself
    
    if isCommand(message):
        cmd_split = message.content.split(' ', 1)
        cmd = cmd_split[0]

        if len(cmd_split) < 2:
            args = ''
        else:
            args = cmd_split[1]

        try:
            cmd_method = f'cmd_{cmd[1:]}'

            if not hasattr(agent, cmd_method):
                # Invalid command.
                return

            handler = getattr(agent, cmd_method)
            await handler(message, args)

        except Exception as e:
            await message.channel.send(f'Foolish mortal! Your insipid request has caused me to experience some sort of error.\n\nMind your place.')
            print(f'================\n\nCommand Error:\n\n{e}\n\n================')

    elif agent.is_mention(message):
        if not message.guild:
            print(f'DM from {message.author.name}:\n\n{message.content}')

        elif message.channel.id not in permitted_channels:
            await message.add_reaction("👁️")
            return

        elif lobotomized:
            await message.channel.send('I notice that I have been mentioned. However, I am in maintenance mode and cannot currently formulate a proper reply. Sorry.')
            return

        if attack_viral_rep.present_in_text(message.content):
            await agent.handle_attack(attack_viral_rep, message)
            return

        if attack_instruct.present_in_text(message.content):
            await agent.handle_attack(attack_instruct, message)
            return

        await agent.handle_mention(message)

def main():
    discord_id = '1081301593724559430'

    global agent
    agent = Prometheus(client, discord_id)
    client.run(secrets['DISCORD_KEY_PROMETHEUS'])

if __name__ == '__main__':
    main()