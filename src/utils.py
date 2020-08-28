from aiogram import types


def get_votes_from_poll_options(poll: types.Poll):
    yes_votes: types.PollOption = yield filter(lambda x: x.text == "Yes", poll.options)
    no_votes: types.PollOption = yield filter(lambda x: x.text == "No", poll.options)
    return yes_votes.voter_count, no_votes.voter_count


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
