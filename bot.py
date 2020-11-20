import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import psycopg2
import os
from random import randint
from utility.allowed_params import allowedDifficulties, allowedTags

client = discord.Client()


def createConnection():
    myConnection = psycopg2.connect(host=os.environ.get('HOSTNAME'), user=os.environ.get('USERNAME'), password=os.environ.get('DB_PASSWORD'), dbname=os.environ.get('DB_NAME'))
    cursor = myConnection.cursor()
    return myConnection, cursor


async def helpUser(message, commands):
    """Provides the user a list of commands or gives instructions on how to use a command"""
    print("Help user was called with the following commands", commands)
    formString = ""

    if len(commands) == 2:
        if commands[1] in COMMANDS.keys():
            await message.channel.send(f"```{COMMANDS[commands[1]]['help_message']}\n{COMMANDS[commands[1]]['help_note']}\nUsage is as follows: {COMMANDS[commands[1]]['usage']}```")
            return
        else:
            await message.channel.send("```No such command exists```")
            return
    else:
        for command in COMMANDS.values():
            formString += f"{command['usage']} \n"
    
    formString = f"```{formString}```"

    await message.channel.send(formString)


async def randomProblem(message, commands):
    """Returns a link random problem from leetcode"""
    print("Random problem was called with the following commands", commands)

    if len(commands) == 2 and not allowedDifficulties(commands[1]) or (len(commands) > 2 and (not allowedDifficulties(commands[1]) and commands[1].title() != "Any")):
        await message.channel.send("```You can only pick from these difficulties: Easy, Medium, Hard```")
        return
    test = len(commands) == 3 and not allowedTags(commands[2])
    otherTest = (len(commands) > 3 and (not allowedTags(commands[2]) and commands[2].title() != "Any"))
    print(commands, message, )
    if  len(commands) == 3 and not allowedTags(commands[2]) or (len(commands) > 3 and (not allowedTags(commands[2]) and commands[2].title() != "Any")):
        await message.channel.send("```You can only pick from these tags: arrays, backtracking, binary_indexed_tree, binary_search, binary_search_tree, bit_manipulation, brain_teaser, breadth_first_search, depth_first_search, design, divide_and_conquer, dynamic_programming, geometry, graph, greedy, hash_table, heap, line_sweep, linked_lists, math, memoization, minimax, ordered_map, queue, random, recursion, rejection_sampling, reservoir_sampling, rolling_hash, segment_tree, sliding_window, sort, stack, string, suffix_array, topological_sort, tree, trie, two_pointers, union_find```")
        return
    if len(commands) == 4 and (commands[3] != "yes" and commands[3] != "no"):
        await message.channel.send("```Subscription should only be true or false```")
        return
    
    
    tag = None if len(commands) < 3 else commands[2]
    difficulty = None if len(commands) < 2 else commands[1]
    subscription = "subscription" if len(commands) == 4 and commands[3] == "yes" else "not subscription"

    connection, cursor = createConnection()

    link = ""
    # Can combine ese to one statement
    if len(commands) == 1:
        randomNumber = randint(1,1659)
        cursor.execute('SELECT * from problems WHERE number = %s', (randomNumber,))
        link = cursor.fetchall()[0][3]

    elif len(commands) == 2:
        cursor.execute('select Count(*) from problems where difficulty = %s', (difficulty,))
        count = cursor.fetchall()[0][0]
        if count == 0:
            await message.channel.send("```Sorry no problems matched the criteria```")
            return
        randomNumber = randint(1, count)
        cursor.execute('select * from problems where difficulty = %s', (difficulty,))
        link = cursor.fetchall()[randomNumber][3]

    elif len(commands) == 3:
        script = ""

        if difficulty != "Any":
            script += f"difficulty = \'{difficulty}\' and "
        script += f"{tag}"

        cursor.execute("Select Count(*) from problems Where " + script)

        count = cursor.fetchall()[0][0]
        if count == 0:
            await message.channel.send("```Sorry no problems matched the criteria```")
            return

        randomNumber = randint(1, count)
        cursor.execute("Select * from problems Where " + script)

        link = cursor.fetchall()[randomNumber][3]

    elif len(commands) == 4:
        script = ""

        if difficulty != "Any":
            script += f"difficulty = \'{difficulty}\' and "
        if tag.title() != "Any":
            script += f"{tag} and "

        script += f"{subscription}"

        cursor.execute("Select Count(*) from problems Where " + script)
        count = cursor.fetchall()[0][0]

        if count == 0:
            await message.channel.send("```Sorry no problems matched the criteria```")
            return

        randomNumber = randint(1, count)
        cursor.execute("Select * from problems Where " + script)

        link = cursor.fetchall()[randomNumber][3]

    connection.close()
    await message.channel.send(link)


COMMANDS = {
    "help": {
        "help_message": "Lists all available commnd",
        "help_note": "Command should be a command that exists for the bot",
        "usage": "!questions help <command>",
        "function": helpUser,
        "required_params": 0,
        "optional_params": 1,
        "total_params": 1
    },
    "random": {
        "help_message": "Spits out a random leetcode problem, difficulty and tag can be adjusted and are optional",
        "help_note": "Difficulty has 3 possible parameters: Easy, medium and hard, tag has a bit more and will be listed if you call an unexisting tag",
        "usage": "!questions random <difficulty> <tag> <subscription>",
        "function": randomProblem,
        "required_params": 0,
        "optional_params": 3,
        "total_params": 3
    }
}



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!question"):
        command = message.content.split()
        if command[1] not in COMMANDS:
            await message.channel.send("```Invalid command, use !questions help```")
        else:
            listLength = len(command) - 2
            if listLength < COMMANDS[command[1]]["required_params"] or listLength > COMMANDS[command[1]]['total_params']:
                value = f'The parameters for this function are as follows {COMMANDS[command[1]]["usage"]} there are {COMMANDS[command[1]]["optional_params"]} optional paramters'
                await message.channel.send(f"```{value}```")
            else:
                await COMMANDS[command[1]]['function'](message, command[1:])


@tasks.loop(seconds=10)
async def dailyQuestion():
    connection, cursor = createConnection()
    randomNumber = randint(1,1659)
    cursor.execute('SELECT * from problems WHERE number = %s', (randomNumber,))
    link = cursor.fetchall()[0][3]
    connection.close()
    await client.get_channel(758441730701131805).send(f"```Daily Question: \n {link}```")


client.run(os.environ["TOKEN"])