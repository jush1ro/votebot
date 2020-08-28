import logging
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types

import sqlite_wrapper as sql_wrapper
import utils


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
                reply: types.Message = await utils.prepare_message(message)
                poll_message: types.Message = await self.send_poll(reply, f"Do you really want to mute "
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
                reply: types.Message = await utils.prepare_message(message)
                poll_message: types.Message = await self.send_poll(reply, f"Do you really want to kick "
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

        @dp.poll_handler()
        async def handle_poll(poll: types.Poll):
            # TODO Use builtin filters for this in handler
            if sql_wrapper.check_poll(self._database_file, poll_id=poll.id):
                if poll.is_closed:
                    poll_data: sql_wrapper.PollData = sql_wrapper.get_poll(self._database_file, poll.id)
                    votes = utils.get_votes_from_poll_options(poll=poll)
                    if votes[0] >= votes[1] * 1.5:  # TODO Create proper customisable function for this
                        await self.sentence_subject(poll_data)
                    else:
                        await self._bot.send_message(poll_data.chat_id,
                                                     text="Users decided against this, what a shame!",
                                                     reply_to_message_id=poll_data.poll_id)
            else:
                pass

        self.dispatcher = dp

    async def send_poll(self, message: types.Message, question: str) -> types.Message:
        """
        Sends poll, just a wrapper for builtin send_poll method of bot
        :param message: message which invoked command to poll
        :param question: which question to use
        :return: message with poll that was sent
        """
        poll_message: types.Message = await self._bot.send_poll(message.chat.id, question=question,
                                                                options=["Yes", "No"],
                                                                close_date=(datetime.now() + timedelta(minutes=1)))
        return poll_message

    async def sentence_subject(self, poll: sql_wrapper.PollData):
        subject_user: types.User = (await self._bot.get_chat_member(poll.chat_id, poll.subject_user_id)).user

        if poll.poll_type == "votekick":
            await self._bot.kick_chat_member(poll.chat_id, poll.subject_user_id,
                                             until_date=(datetime.now() + timedelta(days=7)))
            await self._bot.send_message(chat_id=poll.chat_id,
                                         text=f"User *{subject_user.full_name}* has been kicked for 7 days!",
                                         parse_mode="Markdown")
        elif poll.poll_type == "votemute":
            await self._bot.restrict_chat_member(poll.chat_id, poll.subject_user_id,
                                                 until_date=(datetime.now() + timedelta(days=7)))
            await self._bot.send_message(chat_id=poll.chat_id,
                                         text=f"User *{subject_user.full_name}* has been muted for 7 days!",
                                         parse_mode="Markdown")
