import discord
from discord.ext import commands
import os
from random import randint
from utility.allowed_params import allowedDifficulties, allowedTags
from discord.ext.commands import Bot
# from dotenv import load_dotenv
# load_dotenv()


TOKEN = os.environ.get("TOKEN")



bot = Bot("!")
def createConnection():
    myConnection = psycopg2.connect(host=os.environ.get['HOSTNAME'], user=os.environ.get['USERNAME'], password=os.environ.get['DB_PASSWORD'], dbname=os.environ.get['DB_NAME'] )
    cursor = myConnection.cursor()
    return myConnection, cursor

@bot.command()
async def getRandomProblem(difficulty=None, tag=None):
    print("TEST")
    if difficulty and not allowedDifficulties(difficulty):
        return "You can only pick from these difficulties: Easy, Medium, Hard"
    if tag and not allowedTags(tags):
        return "You can only pick from these tags: Arrays ,Hash_Table ,Linked_Lists ,Math ,Two_Pointers ,String ,Binary_Search ,Divide_and_Conquer ,Dynamic_Programming ,Backtracking ,Stack ,Heap ,Greedy ,Sort ,Bit_Manipulation ,Tree ,Depth_First_Search ,Breadth_First_Search ,Union_Find ,Graph ,Design ,Topological_Sort ,Trie ,Binary_Indexed_Tree ,Segment_Tree ,Binary_Search_Tree ,Recursion ,Brain_Teaser ,Memoization ,Queue ,Minimax ,Reservoir_Sampling ,Ordered_Map ,Geometry ,Random ,Rejection_Sampling ,Sliding_Window ,Line_Sweep ,Rolling_Hash ,Suffix_Array"

    connection, cursor = createConnection()
    link = ""
    if  not difficulty and not tag:
        randomNumber = randInt(1,1659)
        cursor.execute('select * from problems where number = %s, (randomNumber,)')
        link = cursor.fetchall()[0]['link']
    elif difficulty and not tag:
        cursor.execute('select Count(*) as total from problems where difficulty = %s, (difficulty,)')
        count = cursor.fetchall()[0]['total']
        if count == 0:
            return "Sorry no problems matched the criteria"
        randomNumber = randint(1, count)
        cursor.execute('select( * from problems where number = %s, (randomNumber,)')
        link = cursor.fetchall()[0]['link']
    elif tag and not difficulty:
        cursor.execute('select Count(*) as total from problems where tag = %s, (tag,)')
        count = cursor.fetchall()[0]['total']
        if count == 0:
            return "Sorry no problems matched the criteria"
        randomNumber = randint(1, count)
        cursor.execute('select( * from problems where number = %s, (randomNumber,)')
        link = cursor.fetchall()[0]['link']
    elif tag and difficulty:
        cursor.execute('select Count(*) as total from problems where tag = %s and difficulty = %s, (tag, difficulty,)')
        count = cursor.fetchall()[0]['total']
        if count == 0:
            return "Sorry no problems matched the criteria"
        randomNumber = randint(1, count)
        cursor.execute('select( * from problems where number = %s, (randomNumber,)')
        link = cursor.fetchall()[0]['link']
    
    return link

bot.run(TOKEN)