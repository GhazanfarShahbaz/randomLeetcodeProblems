# Discord Leetcode Bot
## Creating Your Own Instance Of This Repo
* Clone the repo : git clone url_here
* When adding to heroku add the following buildpacks
    - https://github.com/heroku/heroku-buildpack-google-chrome
    - https://github.com/heroku/heroku-buildpack-chromedriver
    - heroku/python
* Make sure to set up a heroku database
    - Go to configure addons -> Heroku Postgres
* Follow the enviornment sample and input the data into heroku config vars
    - CHROMEDRIVER_PATH = /app/.chromedriver/bin/chromedriver
    - GOOGLE_CHROME_BIN = /app/.apt/usr/bin/google-chrome
* Make sure to get a token from discord for the bot
* You should be able to deploy now
* Once deployed run any function the bot should able to prefill the database on its own, given that the correct tables have been made

## Current Functions
* !questions help : lists all commands
* !questions random <difficulty> <tag> : picks a random question and returns its link, difficulty, tag and subscription are optional parameters
* !questions information <identifier> : returns information for a problem by number or link
* !questions description <link> : returns the description and code template for a problem by its link
* !questions euler : returns a link to an euler problem
* !questions codechef : returns a link to a codechef problem
* Self updates the database for euler and leetcode problems each month
* Sends a daily leetcode question

## Checklist
- [x] Webscrape data and place it into a csv
- [x] Place data into a database
- [ ] Create bot functions - _In Progress_

## Future Functionalities and Functions
- [x] Function to post a question each day 
- [ ]Save questions that each person in the server has completed
- [ ]Submit answers through message

