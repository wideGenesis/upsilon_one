from datetime import timedelta, datetime
from messages.sql_queries import *


def save_message(msg, fname, sentdatetime, msgtype, parentid=-1):
    if not is_table_exist(MSG_TABLE_NAME):
        create_message_table()
    next_id = get_max_msg_id() + 1
    save_message_to_db(next_id, msg, fname, sentdatetime, msgtype, parentid)
    return next_id


def get_next_id():
    if not is_table_exist(MSG_TABLE_NAME):
        create_message_table()
    next_id = get_max_msg_id() + 1
    return next_id


def update_mailing_lists(msg_id, sentusrdict, failusrdict, pollresult, parent_id=-1):
    if not is_table_exist(MAILING_DATA_TABLE_NAME):
        create_mailing_data_table()
    update_mailing_data(msg_id, sentusrdict, failusrdict, pollresult, parent_id)


def get_mailing_lists(msg_id):
    return get_mailing_data(msg_id)
