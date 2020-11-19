import discord
from os import environ
from random import randint

myConnection = psycopg2.connect(host=environ['HOSTNAME'], user=environ['USERNAME'], password=environ['DB_PASSWORD'], dbname=['DB_NAME'] )

client = discord.Client()
cursor = conn.cursor()


async def getRandomProblem(difficulty=None, tag=None):
    if  not difficulty and not tag:
        randomNumber = randInt(1,1659)
        cursor.execute('select * from problems where number = %s, (randomNumber,))
        return cursor.fetchall()[0]['link']
    # if difficulty and not tag:
    #     cursor.execute('Select Count(*) from problems where difficulty = %s, (difficulty)')
    #     randomNumber = randint(1, cursor.fetchall()[0])
