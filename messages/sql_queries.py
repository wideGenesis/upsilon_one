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
                sbody = ""
                if msgtype == POLL_MESSAGE_TYPE:
                    sbody = json.dumps(body, ensure_ascii=False, encoding='utf8')
                else:
                    sbody = body
                insert_query = f'INSERT INTO {table_name} (msg_id, body, fname, sent_dt, msgtype, parent_id) ' \
                               f'VALUES (\'{msg_id}\', ' \
                               f'\'{sbody}\',\'{fname}\',\'{sent_dt}\',\'{msgtype}\',' \
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
                json_sentusr = ''
                if len(susrdict) > 0:
                    json_sentusr = json.dumps(susrdict)
                json_failusr = ''
                if len(fusrdict) > 0:
                    json_failusr = json.dumps(fusrdict)
                json_pollresult = ''
                if len(presult) > 0:
                    json_pollresult = json.dumps(presult)
                update_query = f'UPDATE {table_name} ' \
                               f'SET sent_usrlist=\'{json_sentusr}\', ' \
                               f'fail_usrlist=\'{json_failusr}\', ' \
                               f'poll_result=\'{json_pollresult}\'' \
                               f'WHERE msg_id=\'{msg_id}\''
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


# ================================= П р о ф а й л е р =================================
def create_user_profiler_data_table(table_name=USER_PROFILER_DATA_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if not is_table_exist(table_name):
            transaction = connection.begin()
            try:
                create_query = f'CREATE TABLE {table_name} ' \
                               f'(usr_id BIGINT NOT NULL, ' \
                               f'final_score INT NOT NULL, ' \
                               f'PRIMARY KEY(usr_id)' \
                               f')'
                connection.execute(create_query)
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
            transaction.commit()


def create_user_profiler_map_table(table_name=USER_PROFILER_MAP_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if not is_table_exist(table_name):
            transaction = connection.begin()
            try:
                create_query = f'CREATE TABLE {table_name} ' \
                               f'(usr_id BIGINT NOT NULL, ' \
                               f'send_poll_id VARCHAR(100), ' \
                               f'qnumber INT NOT NULL, ' \
                               f'PRIMARY KEY(usr_id)' \
                               f')'
                connection.execute(create_query)
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
            transaction.commit()


def user_profiler_data_lookup(usr_id, table_name=USER_PROFILER_DATA_TABLE_NAME, engine=engine) -> bool:
    with engine.connect() as connection:
        try:
            query_string = f'SELECT * FROM {table_name} WHERE usr_id = \'{usr_id}\' LIMIT 1'
            result = connection.execute(query_string)
            return True if result.rowcount > 0 else False
        except:
            return False


def user_profiler_map_lookup(usr_id, table_name=USER_PROFILER_MAP_TABLE_NAME, engine=engine) -> bool:
    with engine.connect() as connection:
        try:
            query_string = f'SELECT * FROM {table_name} WHERE usr_id = \'{usr_id}\' LIMIT 1'
            result = connection.execute(query_string)
            return True if result.rowcount > 0 else False
        except:
            return False


def get_userid_by_pollid(poll_id, table_name=USER_PROFILER_MAP_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        usr_id = None
        qnumber = None
        try:
            query_string = f'SELECT usr_id, qnumber FROM {table_name} WHERE send_poll_id=\'{str(poll_id)}\''
            result = connection.execute(query_string)
            if result.rowcount > 0:
                row = result.fetchone()
                usr_id = row[0]
                qnumber = row[1]
        except:
            return usr_id, qnumber
        return usr_id, qnumber


def update_user_profiler_map(usr_id, poll_id, qnumber, table_name=USER_PROFILER_MAP_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if not is_table_exist(USER_PROFILER_MAP_TABLE_NAME):
            create_user_profiler_map_table()

        transaction = connection.begin()
        if user_profiler_map_lookup(usr_id):
            try:
                del_query = f'DELETE FROM {table_name} WHERE usr_id=\'{usr_id}\''
                connection.execute(del_query)
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
                return
        try:
            insert_query = f'INSERT INTO {table_name} ' \
                           f'(usr_id, send_poll_id, qnumber) ' \
                           f'VALUES (\'{usr_id}\', ' \
                           f'\'{str(poll_id)}\',\'{qnumber}\')'
            connection.execute(insert_query)
            transaction.commit()
        except Exception as e:
            debug(e, ERROR)
            transaction.rollback()
            return


def increment_final_score(user_id, answer_res, table_name=USER_PROFILER_DATA_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if not is_table_exist(USER_PROFILER_DATA_TABLE_NAME):
            create_user_profiler_data_table()

        transaction = connection.begin()
        if not user_profiler_data_lookup(user_id):
            try:
                insert_query = f'INSERT INTO {table_name} ' \
                               f'(usr_id, final_score) ' \
                               f'VALUES (\'{user_id}\', ' \
                               f'\'{answer_res}\')'
                connection.execute(insert_query)
                transaction.commit()
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
                return
        else:
            current_final_score = None
            try:
                query_string = f'SELECT final_score FROM {table_name} WHERE usr_id=\'{user_id}\''
                result = connection.execute(query_string)
                if result.rowcount > 0:
                    current_final_score = result.fetchone()[0]
                update_query = f'UPDATE {table_name} ' \
                               f'SET final_score=\'{current_final_score+answer_res}\' WHERE usr_id=\'{user_id}\''
                connection.execute(update_query)
                transaction.commit()
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
                return


def get_final_score(user_id, table_name=USER_PROFILER_DATA_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if not is_table_exist(USER_PROFILER_DATA_TABLE_NAME):
            create_user_profiler_data_table()
        if not user_profiler_data_lookup(user_id):
            return f'Необходимо пройти опрос!'
        else:
            try:
                query_string = f'SELECT final_score FROM {table_name} WHERE usr_id=\'{user_id}\''
                result = connection.execute(query_string)
                if result.rowcount > 0:
                    current_final_score = result.fetchone()[0]
                    return current_final_score
            except Exception as e:
                debug(e, ERROR)
                return f'Необходимо пройти опрос!'


def reset_user_profiler_data(user_id, table_name=USER_PROFILER_DATA_TABLE_NAME, engine=engine):
    with engine.connect() as connection:
        if not is_table_exist(USER_PROFILER_DATA_TABLE_NAME):
            create_user_profiler_data_table()
        if not user_profiler_data_lookup(user_id):
            return
        else:
            try:
                del_query = f'DELETE FROM {table_name} WHERE usr_id=\'{user_id}\''
                connection.execute(del_query)
                # del_query1 = f'DELETE FROM {USER_PROFILER_MAP_TABLE_NAME} WHERE usr_id=\'{user_id}\''
                # connection.execute(del_query1)
            except Exception as e:
                debug(e, ERROR)


def is_user_profile_done(user_id, engine=engine):
    profile_data_tn = USER_PROFILER_DATA_TABLE_NAME
    profile_map_tn = USER_PROFILER_MAP_TABLE_NAME
    if not is_table_exist(USER_PROFILER_DATA_TABLE_NAME):
        create_user_profiler_data_table()
        return False
    if not is_table_exist(USER_PROFILER_MAP_TABLE_NAME):
        create_user_profiler_map_table()
        return False
    if not user_profiler_data_lookup(user_id):
        return False
    if not user_profiler_map_lookup(user_id):
        return False
    with engine.connect() as connection:
        try:
            query_string = f'SELECT qnumber FROM {profile_map_tn} WHERE usr_id=\'{user_id}\''
            result = connection.execute(query_string)
            if result.rowcount > 0:
                current_qnumber = result.fetchone()[0]
                if current_qnumber == USER_PROFILER_QUESTION_AMOUNT:
                    return True
                else:
                    return False
        except Exception as e:
            debug(e, ERROR)
            return False

