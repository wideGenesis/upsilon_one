from project_shared import *
from datetime import date, timedelta


def is_table_exist(table_name='new_users', engine=engine) -> bool:
    with engine.connect() as connection:
        try:
            query_string = f'SELECT 1 FROM {table_name} LIMIT 1'
            result = connection.execute(query_string)
            return True if result else False
        except:
            return False


def user_lookup(user_id, engine=engine) -> bool:
    with engine.connect() as connection:
        try:
            query_string = f'SELECT * FROM new_users WHERE user_id = \'{user_id}\' LIMIT 1'
            result = connection.execute(query_string)
            return True if result.rowcount > 0 else False
        except:
            return False


def create_newusers_table(table_name='new_users', engine=engine):
    with engine.connect() as connection:
        if not is_table_exist(table_name, engine):
            transaction = connection.begin()
            try:
                create_query = f'CREATE TABLE {table_name} ' \
                               f'(user_id BIGINT NOT NULL, ' \
                               f'username VARCHAR(255), ' \
                               f'append_dt BIGINT NOT NULL, ' \
                               f'wstatus_dt BIGINT, ' \
                               f'PRIMARY KEY(user_id)' \
                               f')'
                connection.execute(create_query)
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
            transaction.commit()


def select_users(engine=engine):
    with engine.connect() as connection:
        users_list = {}
        try:
            query_string = f'SELECT user_id, username, append_dt ' \
                           f'FROM new_users  ' \
                           f'WHERE wstatus_dt IS NULL OR wstatus_dt=\'0\''
            q_result = connection.execute(query_string)
            if q_result.rowcount > 0:
                rows = q_result.fetchall()
                for row in rows:
                    users_list[int(row[0])] = (row[1], int(row[2]))
            else:
                debug("WARNING data is empty", WARNING)
                debug(f"{query_string}", WARNING)
        except Exception as e:
            debug(e, ERROR)
        return users_list


def set_wstatus(user_id, wstatus, engine=engine):
    with engine.connect() as connection:
        if user_lookup(user_id, engine):
            transaction = connection.begin()
            try:
                query_string = f'UPDATE new_users ' \
                               f'SET wstatus_dt=\'{wstatus}\' ' \
                               f'WHERE user_id = \'{user_id}\''
                connection.execute(query_string)
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
            transaction.commit()


def insert_new_user(user_id, username, append_dt, engine=engine):
    with engine.connect() as connection:
        if not user_lookup(user_id, engine):
            transaction = connection.begin()
            try:
                query_string = f'INSERT INTO new_users (user_id, username, append_dt, wstatus_dt) ' \
                               f'VALUES (\'{user_id}\',\'{username}\',\'{append_dt}\',\'NULL\')'
                connection.execute(query_string)
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
            transaction.commit()
