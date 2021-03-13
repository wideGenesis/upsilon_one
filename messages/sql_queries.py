import json
from project_shared import *
from datetime import date, timedelta


def is_table_exist(table_name, engine=engine) -> bool:
    with engine.connect() as connection:
        try:
            query_string = f'SELECT 1 FROM {table_name} LIMIT 1'
            result = connection.execute(query_string)
            return True if result else False
        except:
            return False


def message_lookup(msg_id, table_name=MSG_TABLE_NAME, engine=engine) -> bool:
    with engine.connect() as connection:
        try:
            query_string = f'SELECT * FROM {table_name} WHERE msg_id = \'{msg_id}\' LIMIT 1'
            result = connection.execute(query_string)
            return True if result.rowcount > 0 else False
        except:
            return False


def mailing_data_lookup(msg_id, table_name=MAILING_DATA_TABLE_NAME, engine=engine) -> bool:
    with engine.connect() as connection:
        try:
            query_string = f'SELECT * FROM {table_name} WHERE msg_id = \'{msg_id}\' LIMIT 1'
            result = connection.execute(query_string)
            return True if result.rowcount > 0 else False
        except:
            return False


def create_message_table(table_name=MSG_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if not is_table_exist(table_name):
            transaction = connection.begin()
            try:
                create_query = f'CREATE TABLE {table_name} ' \
                               f'(msg_id BIGINT NOT NULL, ' \
                               f'body TEXT, ' \
                               f'fname  VARCHAR(255), ' \
                               f'sent_dt  DATETIME, ' \
                               f'msgtype INT NOT NULL, ' \
                               f'parent_id BIGINT, ' \
                               f'PRIMARY KEY(msg_id)' \
                               f')'
                connection.execute(create_query)
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
            transaction.commit()


def create_mailing_data_table(table_name=MAILING_DATA_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if not is_table_exist(table_name):
            transaction = connection.begin()
            try:
                create_query = f'CREATE TABLE {table_name} ' \
                               f'(msg_id BIGINT NOT NULL, ' \
                               f'sent_usrlist TEXT, ' \
                               f'fail_usrlist TEXT, ' \
                               f'poll_result  TEXT, ' \
                               f'parent_id BIGINT, ' \
                               f'PRIMARY KEY(msg_id)' \
                               f')'
                connection.execute(create_query)
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
            transaction.commit()


def save_message_to_db(msg_id, body, fname, sent_dt, msgtype, parent_id, table_name=MSG_TABLE_NAME, engine=engine):
    if message_lookup(msg_id):
        debug(f"ERROR: Message with id:{msg_id} is already exist!")
    else:
        with engine.connect() as connection:
            transaction = connection.begin()
            try:
                insert_query = f'INSERT INTO {table_name} (msg_id, body, fname, sent_dt, msgtype, parent_id) ' \
                               f'VALUES (\'{msg_id}\', ' \
                               f'\'{body}\',\'{fname}\',\'{sent_dt}\',\'{msgtype}\',' \
                               f'\'{parent_id}\')'
                connection.execute(insert_query)
                transaction.commit()
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()


def get_mailing_data(msg_id, table_name=MAILING_DATA_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        sentusrdict = {}
        failusrdict = {}
        pollresult = {}
        if mailing_data_lookup(msg_id):
            try:
                sel_query = f'SELECT sent_usrlist, fail_usrlist, poll_result FROM  {table_name} ' \
                            f'WHERE msg_id=\'{msg_id}\''
                result = connection.execute(sel_query)
                sent_usrlist, fail_usrlist, poll_result = result.fetchone()
                if sent_usrlist != '' and sent_usrlist is not None:
                    sentusrdict = json.loads(sent_usrlist)
                if fail_usrlist != '' and fail_usrlist is not None:
                    failusrdict = json.loads(fail_usrlist)
                if poll_result != '' and poll_result is not None:
                    pollresult = json.loads(poll_result)
            except Exception as e:
                debug(e, ERROR)
                return sentusrdict, failusrdict, pollresult
        return sentusrdict, failusrdict, pollresult


def update_mailing_data(msg_id, sentusrdict, failusrdict, pollresult, parent_id,
                        table_name=MAILING_DATA_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        transaction = connection.begin()
        if not mailing_data_lookup(msg_id):
            try:
                json_sentusr = ''
                if len(sentusrdict) > 0:
                    json_sentusr = json.dumps(sentusrdict)
                json_failusr = ''
                if len(failusrdict) > 0:
                    json_failusr = json.dumps(failusrdict)
                json_pollresult = ''
                if len(pollresult) > 0:
                    json_pollresult = json.dumps(pollresult)
                insert_query = f'INSERT INTO {table_name} ' \
                               f'(msg_id, sent_usrlist, fail_usrlist, poll_result, parent_id) ' \
                               f'VALUES (\'{msg_id}\', ' \
                               f'\'{json_sentusr}\',\'{json_failusr}\',\'{json_pollresult}\', \'{parent_id}\')'
                connection.execute(insert_query)
                transaction.commit()
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
        else:
            susrdict, fusrdict, presult = get_mailing_data(msg_id)
            if len(sentusrdict) > 0:
                susrdict.update(sentusrdict)
            if len(failusrdict) > 0:
                fusrdict.update(failusrdict)
            if len(pollresult) > 0:
                presult.update(pollresult) # TODO переделать - надо просто инкрементить результаты, а не заменять их
            try:
                json_sentusr = json.dumps(susrdict)
                json_failusr = json.dumps(fusrdict)
                json_pollresult = json.dumps(presult)
                update_query = f'UPDATE {table_name} ' \
                               f'SET sent_usrlist=\'{json_sentusr}\' ' \
                               f'fail_usrlist=\'{json_failusr}\' ' \
                               f'poll_result=\'{json_pollresult}\'' \
                               f'VALUES (\'{msg_id}\', ' \
                               f'\'{json_sentusr}\',\'{json_failusr}\',\'{json_pollresult}\')'
                connection.execute(update_query)
                transaction.commit()
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()


def get_max_msg_id(table_name=MSG_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        max_id = 50
        if is_table_exist(table_name):
            try:
                sel_query = f'SELECT max(msg_id) FROM  {table_name} '
                result = connection.execute(sel_query)
                bd_max_id =result.fetchone()[0]
                max_id = bd_max_id if bd_max_id is not None else 50
            except Exception as e:
                debug(e, ERROR)
                return max_id
        return max_id

