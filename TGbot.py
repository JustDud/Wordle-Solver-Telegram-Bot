import asyncio
import os

from aiogram import Bot, Dispatcher, types

from handlers.user_private import user_private_router  # Import user-private specific handlers
from common.bot_cmds_list import private  # Import list of bot commands for private chats

from dotenv import find_dotenv, load_dotenv  # Library to load environment variables from a .env file

# Load environment variables from the .env file
load_dotenv(find_dotenv())

# Allowed update types for the bot (messages and edited messages in this case)
ALLOWED_UPDATES = ["message, edited_message"]

# Initialise the bot with the token from the environment variables
bot = Bot(token=os.getenv("TOKEN"))

# Initialise the dispatcher to manage the bot's routing and middleware
dp = Dispatcher()

# Include the user-private router into the dispatcher
dp.include_router(user_private_router)


async def main():
    """
    Main asynchronous entry point for the bot.
    - Deletes any existing webhook to switch to polling.
    - Sets commands for private chats.
    - Starts polling to listen for updates.
    """
    # Remove any active webhook and clear pending updates
    await bot.delete_webhook(drop_pending_updates=True)

    # Set bot commands for all private chats
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())

    # Start the bot's polling loop
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


# Run the main function
asyncio.run(main())
