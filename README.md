# Leetcode Bot
## The Questions Bot is a simple Discord bot that can be used to help users find practice problems for coding exercises.
## If you want to add this bot to your server use the following link: https://discord.com/api/oauth2/authorize?client_id=1004545887965548644&permissions=2048&scope=bot


## Prerequisites
### To use the Questions Bot, you will need to have Python 3 installed on your machine, you then need to install the packages specified in requirements.txt
### You can install these packages by doing the follwoing
``` bash
virtualenv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

# Installation
### To install the Questions Bot, clone the GitHub repository to your local machine and navigate to the project directory:

``` bash
git clonehttps://github.com/GhazanfarShahbaz/leetcode-bot
cd leetcode-bot
```

### Next, create a new file called .env in the project directory and replace all the env_samples. This bot loads environment variables related to sql dynamically, you can edit this by simply putting in your credentials in database/get_db_engine.py. In addition to this, if you dont want to dynamically load the variables just remove all instalces of load_environment() as you will not need it. 

### Make sure to get a discrd bot token from discords developer portal.

### Finally, start the bot by running the following command:

``` bash
python bot.py
```

# Usage
## To use the Questions Bot, simply send a Discord message that begins with !questions, followed by a space and the name of the command you wish to use. For example:

### !questions help
### This will display a list of available commands for the bot.

## Commands
### The following commands are available for the Questions Bot:
- help: Displays a list of available commands for the bot.
- random: Returns a link to a random coding problem from LeetCode.
- euler: Returns a link to a coding problem from Project Euler.
- codechef: Returns a link to a coding problem from CodeChef.

### Each command accepts one or more optional parameters that allow you to filter the results. To view the available parameters for a command, use the help command followed by the name of the command. For example:

### !questions help random

### This will display the available parameters for the random command. You can replace random with any of the commands listed above to get more information on them.

I hope this helps! Feel free to reach out with any questions.
