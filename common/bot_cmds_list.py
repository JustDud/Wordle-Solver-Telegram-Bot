from aiogram.types import BotCommand

# List of bot commands for private chats
# Each BotCommand defines a command and its description, which appears in the bot menu.

private = [
    # Command to start solving a Wordle puzzle
    BotCommand(command='solve', description='Solve the Wordle'),
    # Command to display usage instructions
    BotCommand(command='guide', description='Guide'),
    # Command to show project details
    BotCommand(command='about', description='About the Project')
]