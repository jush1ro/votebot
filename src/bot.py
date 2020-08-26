import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, types

import sqlite_wrapper as sql_wrapper

logging.basicConfig(level=logging.INFO)


async def prepare_message(message: types.Message) -> types.Message:
    """ Prepares message for command and checks whether there is a replied message attached or not
    :param message: message to prepare
    :return: replied message or None
    """
    reply = message.reply_to_message
    if reply is not None:
        return reply
    else:
        await message.reply("Sorry, there doesn't seem to be any reply in your message. "
                            "Please, reply to the message of the user you want to vote on.")


class VoteBot:
    def __init__(self, bot_token: str, database_file: str):
        self._bot: Bot = Bot(token=bot_token)
        self.dispatcher: Dispatcher = Dispatcher(bot=self._bot)
        self._database_file = database_file

        self._setup_handlers()

    def _setup_handlers(self):
        dp: Dispatcher = self.dispatcher

        @dp.message_handler(commands=['start'])
        async def welcome_message(message: types.Message):
            # TODO Check if this is private conversation or group chat
            await self._bot.send_message(message.chat.id, "H3110 w0r1d 42")
            # TODO Make ACTUAL welcome message
            pass

        @dp.message_handler(commands=['votemute'])
        async def votemute(message: types.Message):
            """ Command to vote and mute user
                Works by replying to a message of a user one wants to mute with the command /votemute
                This sends a poll into the chat to kick the user or not
            :param message: message with the command
            :return: None
            """
            try:
                reply: types.Message = await prepare_message(message)
                poll_message: types.Message = await self.send_poll(reply,
                                                                   f"Do you really want to mute "
                                                                   f"{reply.from_user.full_name}?")
                sql_wrapper.insert_poll(self._database_file,
                                        poll_data=sql_wrapper.PollData(poll_id=poll_message.message_id,
                                                                       poll_type="votemute",
                                                                       chat_id=poll_message.chat.id,
                                                                       subject_user_id=message.from_user.id,
                                                                       object_user_id=reply.from_user.id,
                                                                       datetime=datetime.now()))
            except Exception as e:
                logging.debug(e)
                pass

        @dp.message_handler(commands=['votekick'])
        async def votekick(message: types.Message):
            """ Command to vote and kick user
                Works by replying to a message of a user one wants to kick with the command /votekick
                This sends a poll into the chat to kick the user or not
            :param message: message with the command
            :return: None
            """
            try:
                reply: types.Message = await prepare_message(message)
                poll_message: types.Message = await self.send_poll(reply,
                                                                   f"Do you really want to kick "
                                                                   f"{reply.from_user.full_name}?")
                sql_wrapper.insert_poll(self._database_file,
                                        poll_data=sql_wrapper.PollData(poll_id=poll_message.message_id,
                                                                       poll_type="votekick",
                                                                       chat_id=poll_message.chat.id,
                                                                       subject_user_id=message.from_user.id,
                                                                       object_user_id=reply.from_user.id,
                                                                       datetime=datetime.now()))
            except Exception as e:
                logging.debug(e)
                pass

        @dp.poll_answer_handler()
        async def handle_poll_answer(poll_answer: types.PollAnswer):
            # TODO Make this check via builtin filters in aiogram's decorator
            if sql_wrapper.check_poll(self._database_file, poll_id=poll_answer.poll_id):
                # TODO Create logic on new poll answer
                pass
            else:
                # Do nothing if it is not bot's poll
                pass

        self.dispatcher = dp

    async def send_poll(self, reply: types.Message, question: str) -> types.Message:
        poll_message: types.Message = await self._bot.send_poll(reply.chat.id, question=question, options=["Yes", "No"])
        return poll_message
