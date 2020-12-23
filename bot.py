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
from pytz import timezone
from utility.allowed_params import allowedDifficulties, allowedTags, allowedSubscription, subscriptionQuery, allowedCodeChefDifficulty, worksheetName
from utility.messageDict import getLanguageCode, checkLanguage
from utility.tags import getTags
from validators import url
import tempfile
import gspread
import json
import requests
import psycopg2
import os

client = discord.Client()
eulerCount = 735
lastUpdated = -1


def createConnection():
    """Creates connection to the database, returns connection and cursor"""
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn, conn.cursor()


def setupBroswer():
    """Sets up the webdriver, returns the driver so that it can be used"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    return driver


def setupSpreadsheets():
    """Sets up spreadsheets, returns the *not sure what this is yet tbh* """
    authorization_file = tempfile.NamedTemporaryFile()
    authorization_file.write(
        json.dumps(
            {
                "type": os.environ.get("GOOGLE_AUTHORIZATION_TYPE"),
                "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
                "private_key_id": os.environ.get("GOOGLE_PRIVATE_KEY_ID"),
                "private_key": os.environ.get("GOOGLE_PRIVATE_KEY"),
                "client_email": os.environ.get("GOOGLE_CLIENT_EMAIL"),
                "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                "auth_uri": os.environ.get("GOOGLE_AUTH_URI"),
                "token_uri": os.environ.get("GOOGLE_TOKEN_URI"),
                "auth_provider_x509_cert_url": os.environ.get("GOOGLE_AUTH_PROVIDER_X509_CERT_URL"),
                "client_x509_cert_url": os.environ.get("GOOGLE_CLIENT_X509_CERT_URL")
            }
        ).encode('utf-8')
    )
    authorization_file.flush()
    gc = gspread.service_account(filename=authorization_file.name)
    return gc


def getWorksheet(worksheetName: str):
    """Returns a specific worksheet"""
    gc = setupSpreadsheets()
    sheet = gc.open("Leetcode_Bot_Data")

    return sheet.sh.worksheet(worksheetName)


async def numberOfEulerProblems():
    """Checks to the number of euler problems"""
    link = "https://projecteuler.net/recent"
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    global eulerCount
    val = eulerCount
    try:
        val = soup.find('td', class_="id_column").text
        val = int(val)
    except:
        return

    eulerCount = val


async def updateLeetcodeData():
    """Updates the leetcode problems"""

    print("Starting Update")

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
    
    print("Parsing data")
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
        driver.close()
        print("Nothing to add")
        return

    tag_links, corr_tags = getTags()

    print("Parsing tags")
    for tag, link in tag_links.items():
        print("Curremt tag", tag)
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

    try:
        cursor.execute(''' Create Table if not exists problems
        (
            number int,
            name char(156),
            subscription bool,
            link char(156),
            acceptance float,
            difficulty char(32),
            Arrays boolean,
            Hash_Table boolean,
            Linked_Lists boolean,
            Math boolean,
            Two_Pointers boolean,
            String boolean,
            Binary_Search boolean,
            Divide_and_Conquer boolean,
            Dynamic_Programming boolean,
            Backtracking boolean,
            Stack boolean,
            Heap boolean,
            Greedy boolean,
            Sort boolean,
            Bit_Manipulation boolean,
            Tree boolean,
            Depth_First_Search boolean,
            Breadth_First_Search boolean,
            Union_Find boolean,
            Graph boolean,
            Design boolean,
            Topological_Sort boolean,
            Trie boolean,
            Binary_Indexed_Tree boolean,
            Segment_Tree boolean,
            Binary_Search_Tree boolean,
            Recursion boolean,
            Brain_Teaser boolean,
            Memoization boolean,
            Queue boolean,
            Minimax boolean,
            Reservoir_Sampling boolean,
            Ordered_Map boolean,
            Geometry boolean,
            Random boolean,
            Rejection_Sampling boolean,
            Sliding_Window boolean,
            Line_Sweep boolean,
            Rolling_Hash boolean,
            Suffix_Array boolean
        )
        ''')
    except:
        print("Table exists")

    print("Appending data")
    for x, y in data.items():
        cursor.execute("Insert into problems (number, name, subscription, link, acceptance, difficulty, arrays, backtracking, binary_indexed_tree, binary_search, binary_search_tree, bit_manipulation, brain_teaser, breadth_first_search, depth_first_search, design, divide_and_conquer, dynamic_programming, geometry, graph, greedy, hash_table, heap, line_sweep, linked_lists, math, memoization, minimax, ordered_map, queue, random, recursion, rejection_sampling, reservoir_sampling, rolling_hash, segment_tree, sliding_window, sort, stack, string, suffix_array, topological_sort, tree, trie, two_pointers, union_find) Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (x, y['name'], y['subscription'], y['link'], y['acceptance'], y['difficulty'], y['arrays'], y['backtracking'], y['binary_indexed_tree'], y['binary_search'], y['binary_search_tree'], y['bit_manipulation'], y['brain_teaser'], y['breadth_first_search'], y['depth_first_search'], y['design'], y['divide_and_conquer'], y['dynamic_programming'], y['geometry'], y['graph'], y['greedy'], y['hash_table'], y['heap'], y['line_sweep'], y['linked_lists'], y['math'], y['memoization'], y['minimax'], y['ordered_map'], y['queue'], y['random'], y['recursion'], y['rejection_sampling'], y['reservoir_sampling'], y['rolling_hash'], y['segment_tree'], y['sliding_window'], y['sort'], y['stack'], y['string'], y['suffix_array'], y['topological_sort'], y['tree'], y['trie'], y['two_pointers'], y['union_find']))

    connection.commit()
    connection.close()
    print("Finished updating")


async def createSpreadsheets():
    """This only runs if this is the first time creating the sheets"""
    gc = setupSpreadsheets()

    connection, cursor = createConnection()

    sheet = gc.create('Leetcode_Bot_Data')
    number_of_users = len(client.users)

    cursor.execute("Select Count(*) from problems")
    leetcode_count = cursor.fetchone()[0]

    cursor.execute("Select Count(*) from codechef")
    codechef_count = cursor.fetchone()[0]

    connection.close()
    await numberOfEulerProblems()
    global eulerCount

    # creates worksheets
    sheet.add_worksheet(title="Leetcode_Data", rows=str(leetcode_count), cols=str(number_of_users))
    sheet.add_worksheet(title="Codechef_Data", rows=str(codechef_count), cols=str(number_of_users))
    sheet.add_worksheet(title="Euler_Data", rows=str(eulerCount), cols=str(number_of_users))


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
    if len(commands) >= 4 and not allowedSubscription(commands[3]):
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

    script = "where " + params[0] if params else ""

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

    if(len(commands) == 5):
        if commands[4] == "d":
            print(url(link))
            await description(message, [None, link], True)
    # if(len(commands) == 5):
    #     if commands[4] == "i":
    #         await information(message, [None, link])
    #     elif commands[4] == "d":
    #         await description(message, [None, link])
    #     elif commands[4] == 'id' or commands[4] == "di":
    #         await information(message, [None, link])
    #         await information(message, [None, link])



async def information(message, commands, skipCheck=False):
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
        await message.channel.send("Sorry, this is not a valid parameter. You should supply either the problem number or its link")
        connection.close()
        return

    data = cursor.fetchone()[0]

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


async def description(message, commands, skipCheck=False):
    """Returns the description for a questios given a link, need to work on optional param language
        Prbably should add a check to make sure its a leetcode url"""
    if not skipCheck:
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
    link = cursor.fetchall()[randint(1, count)][2]

    connection.close()
    await message.channel.send(link)


def validProblemNumber(problemNumber: int, problemType: str) -> bool:
    if type == "euler":
        global eulerCount
        return True, eulerCount if problemNumber <= eulerCount else False, eulerCount

    connection, cursor = createConnection()

    cursor.execute(f"Select Coun(*) from {problemType}")
    total = cursor.fetchone()[0]

    connection.close()
    return True, total if problemNumber <= total and problemNumber > 0 else False, total


async def completed(message, commands):
    problem_type = message[1].lower()
    problem_number = message[2]
    worksheet_name = worksheetName(problem_type)

    if worksheet_name == "":
        await message.channe.send("This is not a valid type, please pick from leetcode, euler or codechef")
        return

    isValid, total = validProblemNumber(problem_number, problem_type)

    if(not isValid):
        await message.channel.send(f"The given problem number is either too big or too small, the total number of questions for {problem_type} is {total}")
        return

    # Need to do complete logic here
    return


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
        "help_note": "Difficulty has 4 possible parameters: Easy, medium and hard, tag has a bit more and will be listed if you call an unexisting tags, subscription is yes/no and extras is either i, d id or di",
        "usage": "!questions random <difficulty> <tag> <subscription> <extras>",
        "function": randomProblem,
        "required_params": 0,
        "optional_params": 4,
        "total_params": 4
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
    },
    "completed": {
        "help_message": "Marks a question as complete in the spreadsheet",
        "help_note": "From is either leetcode, euler or codechef, number is the problem number that has been completed",
        "usage": "!questions completed <from> <number>",
        "function": completed,
        "required_params": 2,
        "optional_params": 0,
        "total_params": 2
    }
}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    daily.start()
    update.start()


@tasks.loop(minutes=30)
async def daily():
    currentTime = datetime.now(timezone('US/Eastern'))
    if currentTime.hour == 8 and currentTime.minute <= 30:
        channel = client.get_channel(778009190035226634)

        connection, cursor = createConnection()

        cursor.execute("Select Count(*) from problems where subscription = False")
        count = cursor.fetchall()[0][0]

        cursor.execute("Select * from problems where subscription = False")
        link = cursor.fetchall()[randint(1, count)][3]

        connection.close()
        await channel.send(link)


@daily.before_loop
async def beforeStartLoop():
    await client.wait_until_ready()


@tasks.loop(hours=24)
async def update():
    currentMonth = datetime.now().month
    global lastUpdated
    if currentMonth != lastUpdated:
        lastUpdated = currentMonth
        await updateLeetcodeData()
        await numberOfEulerProblems()


@update.before_loop
async def beforeUpdateLoop():
    await client.wait_until_ready()


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


client.run(os.environ["TOKEN"])
