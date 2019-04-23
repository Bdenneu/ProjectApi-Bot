# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from tokens import tokens
from config.functions import *
from config.acces_db import *


class ProjectBot(discord.Client):
    def __init__(self):
        self.token = tokens
        self.bot = discord.Client()
        self.whitelist_channels = [("dev-bot","blabla")]
        self.data = {}

    def catch(self):
        @self.bot.event
        async def on_ready():
            print('Les projets sont prets à etre déclarés!')

        @self.bot.event
        async def on_message(message):
            print(message.channel)
            if (str(message.server),str(message.channel)) in self.whitelist_channels:
                if message[:1] == "{":
                    print("{}: {}".format(message.author,message.content[1:])) 
    def start(self):
        self.catch()
        self.bot.run(self.token)

if __name__ == "__main__":
    bot = ProjectBot()
    bot.start()
