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
    myConnection = psycopg2.connect(host=os.environ.get['HOSTNAME'], user=os.environ.get['USERNAME'], password=os.environ.get['DB_PASSWORD'], dbname=os.environ.get['DB_NAME'])
    cursor = myConnection.cursor()
    return myConnection, cursor


async def randomProblem(commands):
    if len(commands) >= 2 and  allowedDifficulties(commands[1]):
        return "You can only pick from these difficulties: Easy, Medium, Hard"
    if  len(commands) == 3 and not allowedTags(commands[2]):
        return "You can only pick from these tags: Arrays ,Hash_Table ,Linked_Lists ,Math ,Two_Pointers ,String ,Binary_Search ,Divide_and_Conquer ,Dynamic_Programming ,Backtracking ,Stack ,Heap ,Greedy ,Sort ,Bit_Manipulation ,Tree ,Depth_First_Search ,Breadth_First_Search ,Union_Find ,Graph ,Design ,Topological_Sort ,Trie ,Binary_Indexed_Tree ,Segment_Tree ,Binary_Search_Tree ,Recursion ,Brain_Teaser ,Memoization ,Queue ,Minimax ,Reservoir_Sampling ,Ordered_Map ,Geometry ,Random ,Rejection_Sampling ,Sliding_Window ,Line_Sweep ,Rolling_Hash ,Suffix_Array"
    
    tags = None if len(commands) < 3 else commands[2]

    connection, cursor = createConnection()
    link = ""
    if  len(commands) == 1:
        randomNumber = randInt(1,1659)
        cursor.execute('select * from problems where number = %s, (randomNumber,)')
        link = cursor.fetchall()[0]['link']
    elif len(commands) == 2:
        cursor.execute('select Count(*) as total from problems where difficulty = %s, (difficulty,)')
        count = cursor.fetchall()[0]['total']
        if count == 0:
            return "Sorry no problems matched the criteria"
        randomNumber = randint(1, count)
        cursor.execute('select( * from problems where number = %s, (randomNumber,)')
        link = cursor.fetchall()[0]['link']
    elif len(commands) == 3:
        cursor.execute('select Count(*) as total from problems where tag = %s and difficulty = %s, (tag, difficulty,)')
        count = cursor.fetchall()[0]['total']
        if count == 0:
            return "Sorry no problems matched the criteria"
        randomNumber = randint(1, count)
        cursor.execute('select( * from problems where number = %s, (randomNumber,)')
        link = cursor.fetchall()[0]['link']

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