import os
import logging
from bot import VoteBot
from aiogram import executor

logging.basicConfig(level=logging.DEBUG)


def main():
    bot_token = os.environ['BOT_TOKEN']
    logging.debug(f"Obtained BOT_TOKEN from environment variable: {bot_token}")
    database_file = os.environ['DATABASE_FILE']
    logging.debug(f"Obtained DATABASE_FILE from environment variable: {database_file}")
    bot: VoteBot = VoteBot(bot_token=bot_token, database_file=database_file)
    logging.debug(f"Initiated new VoteBot with token: {bot_token}\n and database_file: {database_file}")

    logging.debug(f"Starting polling")
    executor.start_polling(bot.dispatcher, skip_updates=True)


if __name__ == '__main__':
    logging.info("Starting the bot")
    main()
