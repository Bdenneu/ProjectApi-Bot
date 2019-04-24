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
        self.command_list = {"ping":"Answer pong!",
                             "help":"Show list of commands",
                             "show_projects":"Show the list of project",
                             "show_unassigned":"Show the unassigned projects",
                             "whoami":"show what is your nickname in the database",
                             "define_me":"Add/update yourself in the author database"}

    def catch(self):
        @self.bot.event
        async def on_ready():
            print('Projects are soon to be declared!')

        @self.bot.event
        async def on_message(message):
            #If message.guild is undefined, use message.server instead
            if (str(message.guild),str(message.channel)) in self.whitelist_channels:
                if message.content[:1] == "{":
                    list_words = message.content[1:].split(" ")
                    asked_command = list_words[0]
                    if asked_command in self.command_list:
                        if asked_command == "ping":
                            await message.channel.send("pong!")
                        #########################################
                        elif asked_command == "help":
                            answer = "Here is the command list:\n"
                            for i in self.command_list:
                                answer += "**{}**: {}\n".format(i,self.command_list[i])
                            #if message.channel is undefined, use self.bot.send_message
                            await message.channel.send(answer)
                        #########################################
                        elif asked_command == "show_projects":
                            data = db_list_project()
                            answer = ""
                            for i in data:
                                answer += "================\n"
                                answer += "**Name (#{})**: {}".format(i.id,i.name)
                                if len(i.authors) > 0:
                                    answer += "\n**Author(s)**: _{}_".format(i.authors[0].name)
                                    if len(i.authors[1:]) > 0:
                                        for j in i.authors[1:]:
                                            answer += ", _{}_".format(j.name)
                                answer += "\n**Description**: {}\n".format(i.description)
                            await message.channel.send(answer)
                        ########################################
                        elif asked_command == "show_unassigned":
                            data = db_list_unassigned()
                            if data[0]:
                                answer = ""
                                for i in data[1]:
                                    answer += "================\n"
                                    answer += "**Name (#{})**: {}\n".format(i.id,i.name)
                                    answer += "**Description**: {}\n".format(i.description)
                                await message.channel.send(answer)
                            else:
                                await message.channel.send("There are no unassigned projects")
                        #######################################
                        elif asked_command == "whoami":
                            data = db_whoami(message.author.id)
                            if data[0]:
                                await message.channel.send("You are defined in the database as {}".format(data[1].name))
                            else:
                                await message.channel.send("You are not defined in the database")
                        ######################################
                        elif asked_command == "define_me":
                            if not(len(list_words) in [2,3]) :
                                await message.channel.send("Usage: {define\_me _Name_ [_password_]")
                            else:
                                New_author = db_get_author(list_words[1])
                                valid = True
                                if New_author[0]:
                                    pass_needed = func_need_password(New_author[1])
                                    if pass_needed and len(list_words) == 2:
                                        await message.channel.send("A password is needed\nUsage: {define\_me _Name_ [_password_]")
                                        valid = False
                                    elif pass_needed:
                                        valid = func_check_password(New_author.password, list_words[2])
                                        if not(valid):
                                            await message.channel.send("Wrong password")
                                if valid:
                                    Current_author = db_whoami(message.author.id)
                                    if not(Current_author[0]):
                                        new_discord_id = DiscordId(discord_id = str(message.author.id))
                                        session.add(new_discord_id)
                                    else:
                                        new_discord_id = db_get_discordid(str(message.author.id))[1] 
                                    if New_author[0]:
                                        New_author[1].discord_ids += [new_discord_id]
                                        New_author = New_author[1]
                                    elif Current_author[0]:
                                        Current_author[1].name = list_words[1]
                                        New_author = Current_author[1]
                                    else:
                                        New_author = Author(name=list_words[1],discord_ids = [new_discord_id], password = "")
                                        New_author.discord_ids += [new_discord_id]
                                        session.add(New_author)
                                    new_discord_id.author_id = New_author.id
                                    session.commit()
                                    await message.channel.send("Definition done!\nWelcome {}!".format(db_whoami(message.author.id)[1].name))
                    else:
                        await message.channel.send("Command not found: **{}**".format(asked_command)+". Try {help")
                        
    def start(self):
        self.catch()
        self.bot.run(self.token)

if __name__ == "__main__":
    bot = ProjectBot()
    bot.start()
