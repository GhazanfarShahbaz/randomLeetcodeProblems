COMMANDS = {
    "help": {
        "help_message": "Lists all available commnd",
        "usage": "!leetcode_bot help <command>",
        "function": "helpUser",
    },
    "random": {
        "help_message": "Spits out a random leetcode problem, difficulty and tag can be adjusted",
        "usage": "!leetcode_bot random <difficulty> <tag>",
        "function": "randomProblem",
        "required_params": 0,
        "optional_params": 2,
        "total_params": 2
    }
}
