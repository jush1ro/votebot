import sqlite3
from dataclasses import dataclass
from datetime import datetime
from functools import wraps
from sqlite3 import Error


@dataclass
class PollData:
    poll_id: int
    poll_type: str
    chat_id: int
    subject_user_id: int
    object_user_id: int
    datetime: datetime

    def __str__(self):
        return f"{self.poll_id}, {self.poll_type}, {self.chat_id}, " \
               f"{self.subject_user_id}, {self.object_user_id}, {self.datetime}"


def read_poll_record(record):
    return PollData(poll_id=record['poll_id'], poll_type=record['poll_type'], chat_id=record['chat_id'],
                    subject_user_id=record['subject_user_id'], object_user_id=record['object_user_id'],
                    datetime=record['datetime'])


def create_connection(db_file: str) -> sqlite3.Connection:
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def check_poll(db_file: str, poll_id: int) -> bool:
    """ Check whether poll exists in database or not
    :param db_file: database file
    :param poll_id: id of poll
    :return: True if poll exists in database
             False otherwise
    """
    conn = create_connection(db_file)
    with conn:
        cursor = conn.cursor()
        sqlite_query = f"SELECT * FROM POLLS WHERE POLL_ID = {poll_id}"
        cursor.execute(sqlite_query)
        return cursor.fetchone() is not None


# noinspection SqlInsertValues
def insert_poll(db_file: str, poll_data: PollData):
    """ Inserting new poll in database
    :param db_file: database file
    :param poll_data: PollData object of new poll
    :return: None
    """
    conn = create_connection(db_file)
    with conn:
        cursor = conn.cursor()
        sqlite_query = f"INSERT INTO POLLS VALUES ({str(poll_data)})"
        cursor.execute(sqlite_query)


def get_data(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = create_connection(kwargs['db_file'])
        with conn:
            cursor = conn.cursor()
            sqlite_query = func(*args, **kwargs)
            cursor.execute(sqlite_query)
            records = cursor.fetchall()
            if records is not None:
                return [read_poll_record(record) for record in records]

    return wrapper


@get_data
def get_poll(db_file: str, poll_id: int) -> [PollData]:
    """ Get poll by poll's id
    :param db_file: database file
    :param poll_id: id of poll
    :return: PollData of poll or None if no poll was found
    """
    sqlite_query = f"SELECT * from POLLS WHERE POLL_ID = {poll_id}"
    return sqlite_query


@get_data
def get_polls_from_chat(db_file: str, chat_id: int) -> [PollData]:
    """ Get all polls from chat by chat's id
    :param db_file: database file
    :param chat_id: id of chat
    :return: list of PollData of polls or None if no poll was found
    """
    sqlite_query = f"SELECT * from POLLS WHERE CHAT_ID = {chat_id}"
    return sqlite_query


@get_data
def get_subject_user_polls(db_file: str, subject_user_id: int) -> [PollData]:
    """ Get all polls with said subject user by user's id
    :param db_file: database file
    :param subject_user_id: id of subject user
    :return: list of PollData of polls or None if no poll was found
    """
    sqlite_query = f"SELECT * from POLLS WHERE SUBJECT_USER_ID = {subject_user_id}"
    return sqlite_query


@get_data
def get_object_user_polls(db_file: str, object_user_id: int) -> [PollData]:
    """ Get all polls with said object user by user's id
    :param db_file: database file
    :param object_user_id: id of object user
    :return: list of PollData of polls or None if no poll was found
    """
    sqlite_query = f"SELECT * from POLLS WHERE OBJECT_USER_ID = {object_user_id}"
    return sqlite_query
