import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from random import randint
from datetime import datetime
from utility.allowed_params import allowedDifficulties, allowedTags, allowedSubscription, subscriptionQuery, allowedCodeChefDifficulty
from utility.messageDict import getLanguageCode, checkLanguage
from utility.tags import getTags
from validators import url
import psycopg2
import os


# googlesheets -> gspread -> pandas


client = discord.Client()
eulerCount = 735
eulerlastUpdated = -1
leetcodelastUpdated = -1

def createConnection():
    """Creates connection to the database, returns connection and cursor"""
    myConnection = psycopg2.connect(host=os.environ.get('HOSTNAME'), user=os.environ.get('USERNAME'), password=os.environ.get('DB_PASSWORD'), dbname=os.environ.get('DB_NAME'))
    cursor = myConnection.cursor()
    return myConnection, cursor


def setupBroswer():
    """Sets up the webdriver, returns the driver so that it can be used"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    return driver

def numberOfEulerProblems():
    """Checks to the number of euler problems"""
    currentMonth = datetime.now().month
    global eulerlastUpdated
    if currentMonth != eulerlastUpdated:
        link = "https://projecteuler.net/recent"
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        val = 0
        try:
            val = soup.find('td', class_="id_column").text
        except:
            return
        global eulerCount
        eulerCount = val
        eulerlastUpdated = currentMonth

async def updateLeetcodeData(message):
    """Updates the leetcode problems"""
    currentMonth = datetime.now().month
    global leetcodelastUpdated
    if currentMonth != leetcodelastUpdated:
        await message.channel.send("Updating, this might take awhile")
        leetcodelastUpdated = currentMonth
        connection, cursor = createConnection()
        cursor.execute("Select Count(*) from problems")
        totalCount = cursor.fetchone()[0]
        connection.close()

        driver = setupBroswer()

        driver.get("https://leetcode.com/problemset/all/")
        driver.find_element_by_xpath('//select[@class = "form-control"]').click()
        select = Select(driver.find_element_by_xpath('//select[@class = "form-control"]'))
        select.select_by_visible_text('all')

        data = {}

        start = True
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        
        for trTags in soup.find_all("tr"):
            if(start):
                start = False
                continue
            else:
                parser = 0
                currentNumber = 0
                for row in trTags.find_all('td'):
                    if parser == 1:
                        currentNumber = row.text.strip()
                        currentNumber = int(currentNumber)
                        if(currentNumber < totalCount):
                            break 
                        data[currentNumber] = {'arrays': False, 'backtracking': False, 'binary_indexed_tree': False, 'binary_search': False, 'binary_search_tree': False, 'bit_manipulation': False, 'brain_teaser': False, 'breadth_first_search': False, 'depth_first_search': False, 'design': False, 'divide_and_conquer': False, 'dynamic_programming': False, 'geometry': False, 'graph': False, 'greedy': False, 'hash_table': False, 'heap': False, 'line_sweep': False, 'linked_lists': False, 'math': False, 'memoization': False, 'minimax': False, 'ordered_map': False, 'queue': False, 'random': False, 'recursion': False, 'rejection_sampling': False, 'reservoir_sampling': False, 'rolling_hash': False, 'segment_tree': False, 'sliding_window': False, 'sort': False, 'stack': False, 'string': False, 'suffix_array': False, 'topological_sort': False, 'tree': False, 'trie': False, 'two_pointers': False, 'union_find': False}
                    elif parser == 2:
                        val = ""
                        for x in row.text.strip():
                            if x.isalnum() or x==" ":       
                                val +=x
                            else:
                                val += "_"

                        data[currentNumber]["name"] = val
                        data[currentNumber]["subscription"] = False if len(row.findChild().contents) == 2 else True
                        data[currentNumber]["link"] = f"https://leetcode.com{row.findChild().findChild()['href']}"
                    elif parser == 4:
                        data[currentNumber]["acceptance"] = row.text[:len(row.text)-1]
                    elif parser == 5:
                        data[currentNumber]["difficulty"] = row.text
                        break
                    parser += 1 

        if not data:
            await message.channel.send("Up to date")
            driver.close()
            return

        tag_links, corr_tags = getTags()

        for tag, link in tag_links.items():
            driver.close()
            driver = setupBroswer()
            driver.get(link)
            try:
                Select(driver.find_element_by_xpath('//select[@class = "form-control"]'))
            except:
                pass
            try:
                driver.find_element_by_xpath('//select[@class = "form-control"]').click()
                select = Select(driver.find_element_by_xpath('//select[@class = "form-control"]'))
                select.select_by_visible_text('all')
            except:
                pass

            start = True
            soup = BeautifulSoup(driver.page_source, features="html.parser")

            for trTags in soup.find_all("tr"):
                if(start):
                    start = False
                    continue
                else:
                    parser = 0
                    for row in trTags.find_all('td'):
                        if parser == 1:
                            currentNumber = row.text.strip()
                            currentNumber = int(currentNumber)
                            if currentNumber in data.keys():
                                data[currentNumber][corr_tags[tag]] = True
                        parser += 1 
        driver.close()
        connection, cursor = createConnection()
        for x, y in data.items():
            cursor.execute("Insert into problems (number, name, subscription, link, acceptance, difficulty, arrays, backtracking, binary_indexed_tree, binary_search, binary_search_tree, bit_manipulation, brain_teaser, breadth_first_search, depth_first_search, design, divide_and_conquer, dynamic_programming, geometry, graph, greedy, hash_table, heap, line_sweep, linked_lists, math, memoization, minimax, ordered_map, queue, random, recursion, rejection_sampling, reservoir_sampling, rolling_hash, segment_tree, sliding_window, sort, stack, string, suffix_array, topological_sort, tree, trie, two_pointers, union_find) Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, )", (x, y['name'], y['subscription'], y['link'], y['acceptance'], y['difficulty'], y['arrays'], y['backtracking'], y['binary_indexed_tree'], y['binary_search'], y['binary_search_tree'], y['bit_manipulation'], y['brain_teaser'], y['breadth_first_search'], y['depth_first_search'], y['design'], y['divide_and_conquer'], y['dynamic_programming'], y['geometry'], y['graph'], y['greedy'], y['hash_table'], y['heap'], y['line_sweep'], y['linked_lists'], y['math'], y['memoization'], y['minimax'], y['ordered_map'], y['queue'], y['random'], y['recursion'], y['rejection_sampling'], y['reservoir_sampling'], y['rolling_hash'], y['segment_tree'], y['sliding_window'], y['sort'], y['stack'], y['string'], y['suffix_array'], y['topological_sort'], y['tree'], y['trie'], y['two_pointers'], y['union_find'],))

        connection.commit()
        connection.close()
        await message.channel.send("Up to date")


    


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

    if len(commands) >=2 and not allowedDifficulties(commands[1]):
        await message.channel.send("```You can only pick from these difficulties: Any, Easy, Medium, Hard```")
        return
    if len(commands) >=3 and not allowedTags(commands[2]):
        await message.channel.send("```You can only pick from these tags: any, arrays, backtracking, binary_indexed_tree, binary_search, binary_search_tree, bit_manipulation, brain_teaser, breadth_first_search, depth_first_search, design, divide_and_conquer, dynamic_programming, geometry, graph, greedy, hash_table, heap, line_sweep, linked_lists, math, memoization, minimax, ordered_map, queue, random, recursion, rejection_sampling, reservoir_sampling, rolling_hash, segment_tree, sliding_window, sort, stack, string, suffix_array, topological_sort, tree, trie, two_pointers, union_find```")
        return
    if len(commands) == 4 and not allowedSubscription(commands[3]):
        await message.channel.send("```Subscription should be true, false or any```")
        return

    connection, cursor = createConnection()

    difficulty = "Any" if len(commands) < 2 else commands[1].title()
    tag = "Any" if len(commands) < 3 else commands[2]
    subscription = "Any" if len(commands) < 4 else subscriptionQuery(commands[3])

    params =[]
    params.append(f"difficulty = \'{difficulty}\'") if difficulty.lower() != "any" else None
    params.append(tag) if tag.lower() != "any" else None
    params.append(subscription) if subscription.lower() != "any" else None

    script = "where " +params[0] if params else ""

    for x in range(1, len(params)):
        script += f" and {params[x]} "

    print("Select * from problems " + script)

    cursor.execute("Select Count(*) from problems " + script)
    count = cursor.fetchall()[0][0]
    if(count == 0):
        await message.channel.send("```Sorry no problems matched the criteria```")
        return

    cursor.execute("Select * from problems " + script)
    link = cursor.fetchall()[randint(1,count)][3]
    connection.close()
    await message.channel.send(link)


async def information(message, commands):
    """Returns information for a proble given a link or problem number"""
    print("Information function was called with the following parameters: ", commands)
    connection, cursor = createConnection()
    if commands[1].isnumeric():
        value = int(commands[1])
        cursor.execute("select * from problems where number = %s", (value,))
    elif url(commands[1]):
        thisUrl = commands[1]
        cursor.execute("select * from problems where link = %s", (thisUrl,))
    else:
        message.channel.send("Sorry, this is not a valid parameter. You should supply either the problem number or its link")
        connection.close()
        return

    data = cursor.fetchone()

    if not data:
        message.channel.send("Sorry this link/number does not exist")
        connection.close()
        return
    colNames = [val[0] for val in cursor.description]
    foundFirstType = False
    formString = "```\n"

    for i in range(len(colNames)):
        if i > 5 and not data[i]:
            pass
        elif i > 5 and data[i] and not foundFirstType:
            foundFirstType = True
            formString += f"Problem Tags: {colNames[i]}"
        elif i > 5:
            formString += f", {colNames[i]}"
        else:
            formString += f"{colNames[i].title()}: {data[i]}\n"

    if not foundFirstType:
        formString += "Problem Tags: None"
    
    formString += "\n```"
    connection.close()

    await message.channel.send(formString)    


async def description(message, commands):
    """Returns the description for a questios given a link, need to work on optional param language
        Prbably should add a check to make sure its a leetcode url"""
    if not url(commands[1]):
        await message.channel.send("Sorry this is not a valid url")
        return
    if len(commands) == 3 and not checkLanguage(commands[2]):
        await message.channel.send("Sorry this is not a valid language")
        return
    
    connection, cursor = createConnection()

    cursor.execute("Select subscription from problems where link = %s", (commands[1],))
    data = cursor.fetchone()[0]
    connection.close()

    if(data):
        await message.channel.send("```Sorry this question requires a subscription```")
        return


    print("Template function was called with the following parameters:", commands)
    
    driver = setupBroswer()
    print(commands[1])
    driver.get(commands[1])

    soup = BeautifulSoup(driver.page_source, features="html.parser")

    problem = "```ts\n"
    for x in soup.find_all("div", class_="content__u3I1 question-content__JfgR"):
        problem += x.text + "\n"
    problem += "```"

    await message.channel.send(problem)

    language = "Python3" if len(commands) < 3 else commands[2].title()
    xpath = f'//li[@data-cy=\"lang-select-{language.title()}\"]'

    driver.find_element_by_xpath('//span[@class="ant-select-arrow"]').click()

    element = driver.find_element_by_xpath(xpath)
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()

    driver.find_element_by_xpath(xpath).click()

    soup = BeautifulSoup(driver.page_source, features="html.parser")
    code_block = soup.find_all('span', {"role": "presentation"})

    template = f"```{getLanguageCode(language)}\n"
    for x in code_block:
        template += x.text + "\n"
    template += "```"

    driver.close()

    await message.channel.send(template)


async def euler(message, commands):
    numberOfEulerProblems()
    global eulerCount
    await message.channel.send(f"https://projecteuler.net/problem={randint(1,eulerCount)}")


async def codechef(message, commands):
    """Returns a link to a question from codechef, will be adding other comands"""
    if len(commands) == 2 and not allowedCodeChefDifficulty(commands[1]):
        await message.channel.send("```This is not a valid difficulty. Please pick from the following: beginner, easy, medium, hard, challenger```") 
        return

    connection, cursor = createConnection()
    script = "" if len(commands) == 1 else f" where difficulty = \'{commands[1]}\' "

    cursor.execute("Select Count(*) from codechef" + script)
    count = cursor.fetchall()[0][0]
    cursor.execute("Select * from codechef" + script)
    link = cursor.fetchall()[randint(1,count)][2]

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
    },
    "information": {
        "help_message": "Spits out information for a given question number or link",
        "help_note": "Identifier can either be a number or a link",
        "usage": "!questions information <identifier>",
        "function": information,
        "required_params": 1,
        "optional_params": 0,
        "total_params": 1
    },
    "description": {
        "help_message": "Returns the template for a question given a link",
        "help_note": "Link that is meant to be looked at, language that the template should be in",
        'usage': "!questions description <link> <language>",
        "function": description,
        "required_params": 1,
        "optional_params": 1,
        "total_params": 2
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
        "help_note": "Optional param difficulty: pick from the following beginner, easy, medium, hard, challenge ",
        "usage": "!questions codechef <difficulty>",
        "function": codechef,
        "required_params": 0,
        "optional_params": 1,
        "total_params": 1
    }
}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    """Reads the message and calls the necessary function"""
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
    await updateLeetcodeData(message)

client.run(os.environ["TOKEN"])
