import discord
from discord.ext import commands
import os
from random import randint
from utility.allowed_params import allowedDifficulties, allowedTags
from discord.ext.commands import Bot
from dotenv import load_dotenv
import psycopg2
load_dotenv()

client = discord.Client()
def createConnection():
    myConnection = psycopg2.connect(host=os.environ.get('HOSTNAME'), user=os.environ.get('USERNAME'), password=os.environ.get('DB_PASSWORD'), dbname=os.environ.get('DB_NAME'))
    cursor = myConnection.cursor()
    return myConnection, cursor


async def randomProblem(commands):
    if len(commands) >= 2 and  allowedDifficulties(commands[1]):
        return "You can only pick from these difficulties: Easy, Medium, Hard"
    if  len(commands) == 3 and not allowedTags(commands[2]):
        return "You can only pick from these tags: arrays, backtracking, binary_indexed_tree, binary_search, binary_search_tree, bit_manipulation, brain_teaser, breadth_first_search, depth_first_search, design, divide_and_conquer, dynamic_programming, geometry, graph, greedy, hash_table, heap, line_sweep, linked_lists, math, memoization, minimax, ordered_map, queue, random, recursion, rejection_sampling, reservoir_sampling, rolling_hash, segment_tree, sliding_window, sort, stack, string, suffix_array, topological_sort, tree, trie, two_pointers, union_find"
    
    tags = None if len(commands) < 3 else commands[2]

    connection, cursor = createConnection()
    link = ""
    if  len(commands) == 1:
        randomNumber = randint(1,1659)
        cursor.execute('SELECT * from problems WHERE number = %s', (randomNumber,))
        link = cursor.fetchall()[0][3]
    elif len(commands) == 2:
        cursor.execute('select Count(*) as total from problems where difficulty = %s', (difficulty,))
        count = cursor.fetchall()[0][0]
        if count == 0:
            return "Sorry no problems matched the criteria"
        randomNumber = randint(1, count)
        cursor.execute('select * from problems where number = %s', (randomNumber,))
        link = cursor.fetchall()[0][3]
    elif len(commands) == 3:
        script = f"select Count(*) as total from problems where difficulty = \'{difficulty}\' and {tag}"
        cursor.execute(script)
        count = cursor.fetchall()[0][0]
        if count == 0:
            return "Sorry no problems matched the criteria"
        randomNumber = randint(1, count)
        cursor.execute('select * from problems where number = %s', (randomNumber,))
        link = cursor.fetchall()[0][3]

    await message.channel.send(link)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


COMMANDS = {
    "help": {
        "help_message": "Lists all available commnd",
        "usage": "!leetcode_bot help <command>",
        "function": "helpUser",
    },
    "random": {
        "help_message": "Spits out a random leetcode problem, difficulty and tag can be adjusted",
        "usage": "!leetcode_bot random <difficulty> <tag>",
        "function": randomProblem,
        "required_params": 0,
        "optional_params": 2,
        "total_params": 2
    }
}


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!leetcode_bot"):
        command = message.content.split()
        if command[1] not in COMMANDS:
            await message.channel.send('Invalid command, use !leetcode_bot help')
        else:
            listLength = len(command) - 2
            if listLength < COMMANDS[command[1]]["required_params"] or listLength > COMMANDS[command[1]]['total_params']:
                await message.channel.send(f'The parameters for this function are as follows {COMMANDS[command[1]]["usage"]} there are {COMMANDS[command[1]]["optional_params"]} optional paramters')
            else:
                await COMMANDS[command[1]]['function'](command[1:])

client.run(os.environ["TOKEN"])