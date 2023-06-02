import discord


from dotenv import load_dotenv

from os import getenv

from random import randint

from database.codechef_question_repository import CodeChefQuestionRepository
from database.leetcode_question_repository import LeetCodeQuestionRepository

from utility.allowed_params import allowedDifficulties, allowedTags, allowedSubscription, subscriptionQuery, allowedCodeChefDifficulty, worksheetName
from utility.messageDict import getLanguageCode, checkLanguage
from utility.tags import getTags
   
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
eulerCount = 735


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

async def helpUser(message, commands):
    """Provides the user a list of commands or gives instructions on how to use a command"""
    print("Help user was called with the following commands: ", commands)
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
    print("Random problem was called with the following commands: ", commands)

    if len(commands) >= 2 and not allowedDifficulties(commands[1]):
        await message.channel.send("```You can only pick from these difficulties: Any, Easy, Medium, Hard```")
        return
    if len(commands) >= 3 and not allowedTags(commands[2]):
        await message.channel.send("```You can only pick from these tags: any, arrays, backtracking, binary_indexed_tree, binary_search, binary_search_tree, bit_manipulation, brain_teaser, breadth_first_search, depth_first_search, design, divide_and_conquer, dynamic_programming, geometry, graph, greedy, hash_table, heap, line_sweep, linked_lists, math, memoization, minimax, ordered_map, queue, random, recursion, rejection_sampling, reservoir_sampling, rolling_hash, segment_tree, sliding_window, sort, stack, string, suffix_array, topological_sort, tree, trie, two_pointers, union_find```")
        return
    if len(commands) >= 4 and not allowedSubscription(commands[3]):
        await message.channel.send("```Subscription should be yes, no, or any```")
        return
    
    difficulty = [] if len(commands) < 2 else [commands[1].title()]
    if difficulty and difficulty[0] == "Any":
        difficulty = []
        
    tags = [] if len(commands) < 3 else [commands[2]]
    if tags and tags[0] == "Any":
        tags = []
        
    subscription_temp_str: str = None if len(commands) < 4 else subscriptionQuery(commands[3])
    subscription = None
    if subscription_temp_str and not subscription_temp_str == "any":
        subscription = True if subscription_temp_str.lower() == "yes" else False
    
    filterForm: dict = {
        "difficulty": difficulty,
        "tags": tags,
        "subscription": subscription
    }
    
    result = None
    with LeetCodeQuestionRepository() as repository:
        result = repository.filter_and_get_random(filterForm)
        
    await message.channel.send(result.link)


async def codechef(message, commands):
    """Returns a link to a question from codechef, will be adding other comands"""
    if len(commands) == 2 and not allowedCodeChefDifficulty(commands[1]):
        await message.channel.send("```This is not a valid difficulty. Please pick from the following: beginner, easy, medium, hard, challenge```")
        return

    result = None 
    
    filter_form = {
        "difficulty": [] if len(commands) < 2 else [commands[1].lower()]
    }
    
    
    with CodeChefQuestionRepository() as repository:
        result = repository.filter_and_get_random(filter_form)
    
    await message.channel.send(result.link)


async def euler(message, commands):
    global eulerCount
    await message.channel.send(f"https://projecteuler.net/problem={randint(1,eulerCount)}")


COMMANDS = {
    "help": {
        "help_message": "Lists all available commnd",
        "help_note": "Command should be a command that exists for the bot",
        "usage": "$questions help <command>",
        "function": helpUser,
        "required_params": 0,
        "optional_params": 1,
        "total_params": 1
    },
    "random": {
        "help_message": "Spits out a random leetcode problem, difficulty and tag can be adjusted and are optional",
        "help_note": "Difficulty has 4 possible parameters: Easy, medium and hard, tag has a bit more and will be listed if you call an unexisting tags, subscription is yes/no and extras is either i, d id or di (extras is currently under maintenance)",
        "usage": "!questions random <difficulty> <tag> <subscription> <extras>",
        "function": randomProblem,
        "required_params": 0,
        "optional_params": 4,
        "total_params": 4
    },
    "euler": {
        "help_message": "Returns a link to a question from the euler project",
        "help_note": "No params needed",
        "usage": "!questions euler",
        "function": euler,
        "required_params": 0,
        "optional_params": 0,
        "total_params": 0
    },
    "codechef": {
        "help_message": "Returns a link to a question from codechef",
        "help_note": "Optional param difficulty: pick from the following beginner, easy, medium, hard, challenge",
        "usage": "!questions codechef <difficulty>",
        "function": codechef,
        "required_params": 0,
        "optional_params": 1,
        "total_params": 1
    }
}


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$questions'):
        command = message.content.split()
        
        if command[1] not in COMMANDS:
            await message.channel.send("```Invalid command, use !questions help```")
        else:
            listLength = len(command) - 2
            if listLength < COMMANDS[command[1]]["required_params"] or listLength > COMMANDS[command[1]]['total_params']:
                value = f'The parameters for this function are as follows {COMMANDS[command[1]]["usage"]} there are {COMMANDS[command[1]]["optional_params"]} optional paramters'
                await message.channelsend(f"```{value}```")
            else:
                await COMMANDS[command[1]]['function'](message, command[1:])


client.run(getenv("DISCORD_TOKEN"))
