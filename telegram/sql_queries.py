import json

from project_shared import *


async def user_search(identifier, engine=None):
    with engine.connect() as connection:
        result = connection.execute("SELECT * FROM  entities WHERE id = %s", [identifier])
        return result.cursor.fetchone()


async def db_save_lang(value, identifier, engine=None):
    with engine.connect() as connection:
        result = connection.execute("UPDATE entities SET profile_lang = %s WHERE id = %s", [value, identifier])
        return result.cursor.fetchone()


async def db_save_expired_data(expired, level, identifier, engine=None):
    with engine.connect() as connection:
        result = connection.execute("UPDATE entities SET expired = %s, subscribe_level = %s WHERE id = %s",
                                    [expired, level, identifier])
        return result.cursor.fetchone()


async def db_save_referral(value, identifier, engine=None):
    with engine.connect() as connection:
        connection.execute("UPDATE entities SET referral = %s WHERE id = %s", [value, identifier])
        connection.execute("commit")


async def db_save_risk_profile(value, identifier, engine=None):
    with engine.connect() as connection:
        is_exist = await is_table_exist('risk_profile_data', engine)
        if not is_exist:
            await create_risk_profile_data_table(engine)
        transaction = connection.begin()
        try:
            if risk_data_lookup(identifier):
                sql_query = f'UPDATE risk_profile_data SET rdata = concat(rdata, \'{value}\') WHERE user_id = \'{identifier}\''
            else:
                sql_query = f'INSERT INTO risk_profile_data ' \
                           f'(user_id, rdata) ' \
                           f'VALUES (\'{identifier}\', \'{value}\')'
            debug(f"SQL QUERY: {sql_query} ")
            connection.execute(sql_query)
            transaction.commit()
        except Exception as e:
            debug(e, ERROR)
            transaction.rollback()


async def create_risk_profile_data_table(engine=None):
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            connection.execute("CREATE TABLE risk_profile_data ("
                               "user_id BIGINT NOT NULL, "
                               "rdata VARCHAR(255) NOT NULL, "
                               "PRIMARY KEY(user_id)"
                               ")")
            transaction.commit()
        except Exception as e:
            debug(e, ERROR)
            transaction.rollback()


def risk_data_lookup(user_id, engine=engine) -> bool:
    with engine.connect() as connection:
        try:
            query_string = f'SELECT * FROM risk_profile_data WHERE user_id = \'{user_id}\' LIMIT 1'
            debug(f"SQL QUERY LOOKUP: {query_string} ")
            result = connection.execute(query_string)
            return True if result.rowcount > 0 else False
        except Exception as e:
            debug(e, ERROR)
            return False


async def create_payment_message_table(engine=None):
    with engine.connect() as connection:
        is_exist = await is_table_exist('payment_message_hist', engine)
        if not is_exist:
            connection.execute("CREATE TABLE payment_message_hist ("
                               "order_id VARCHAR(255) NOT NULL, "
                               "user_id BIGINT NOT NULL, "
                               "msg_id BIGINT NOT NULL, "
                               "create_dt BIGINT NOT NULL, "
                               "PRIMARY KEY(order_id, user_id, msg_id)"
                               ")")
            connection.execute("commit")


async def delete_from_payment_message(order_id, engine=None):
    with engine.connect() as connection:
        connection.execute("DELETE from payment_message_hist WHERE order_id = %s", order_id)
        connection.execute("commit")


async def insert_into_payment_message(order_id, sender_id, msg_id, dt_int, engine=None):
    with engine.connect() as connection:
        connection.execute("INSERT INTO payment_message_hist(order_id, user_id, msg_id, create_dt) "
                           "VALUES( %s, %s, %s, %s )", [order_id, sender_id, msg_id, dt_int])
        connection.execute("commit")


async def get_all_payment_message(engine=None):
    with engine.connect() as connection:
        result = connection.execute("SELECT order_id, user_id, msg_id, create_dt FROM  payment_message_hist")
        rows = result.cursor.fetchall()
        return rows


async def is_table_exist(table_name, engine=engine) -> bool:
    with engine.connect() as connection:
        try:
            query_string = "SELECT 1 FROM " + table_name + " LIMIT 1"
            result = connection.execute(query_string)
            return True if result else False
        except:
            return False


async def get_all_users(engine=None):
    with engine.connect() as connection:
        users = []
        try:
            query_string = f'SELECT id FROM entities'
            q_result = connection.execute(query_string)
            if q_result.rowcount > 0:
                rows = q_result.fetchall()
                for row in rows:
                    if row[0] not in EXCLUDE_USERS:
                        users.append(row[0])
        except Exception as e:
            debug(e, ERROR)
    return users


async def create_donate_data_table(engine=engine):
    with engine.connect() as connection:
        ite = await is_table_exist(DONATE_DATA_TABLE_NAME, engine)
        if not ite:
            transaction = connection.begin()
            try:
                create_query = f'CREATE TABLE {DONATE_DATA_TABLE_NAME} ' \
                               f'(dateTime DATETIME NOT NULL, ' \
                               f'user_id  BIGINT NOT NULL, ' \
                               f'sum DOUBLE NOT NULL, ' \
                               f'PRIMARY KEY(dateTime, user_id)' \
                               f')'
                connection.execute(create_query)
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
            transaction.commit()


async def save_donate_data(sender_id, summa):
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            now = datetime.datetime.now()
            connection.execute(f"INSERT INTO donate_data(dateTime, user_id, sum)  "
                               f"VALUES( \'{now}\', \'{sender_id}\', \'{summa}\')")
        except Exception as e:
            debug(e, ERROR)
            transaction.rollback()
        transaction.commit()


async def create_last_action_table(engine=engine):
    with engine.connect() as connection:
        ite = await is_table_exist(LAST_ACTION_TABLE_NAME, engine)
        if not ite:
            transaction = connection.begin()
            try:
                create_query = f'CREATE TABLE {LAST_ACTION_TABLE_NAME} ' \
                               f'(user_id  BIGINT NOT NULL, ' \
                               f'dateTime DATETIME NOT NULL, ' \
                               f'action_type VARCHAR(100) NOT NULL, ' \
                               f'action VARCHAR(100) NOT NULL, ' \
                               f'PRIMARY KEY(user_id)' \
                               f')'
                connection.execute(create_query)
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
            transaction.commit()


async def last_action_lookup(user_id, engine=engine) -> bool:
    with engine.connect() as connection:
        try:
            query_string = f'SELECT * FROM {LAST_ACTION_TABLE_NAME} WHERE user_id = \'{user_id}\' LIMIT 1'
            result = connection.execute(query_string)
            return True if result.rowcount > 0 else False
        except Exception as e:
            debug(e, ERROR)
            return False


async def save_action_data(user_id, action_type, action):
    with engine.connect() as connection:
        ite = await is_table_exist(LAST_ACTION_TABLE_NAME, engine)
        if not ite:
            await create_last_action_table(engine)
        transaction = connection.begin()
        try:
            now = datetime.datetime.now()
            lal = await last_action_lookup(user_id)
            if lal:
                connection.execute(f"UPDATE {LAST_ACTION_TABLE_NAME} "
                                   f"SET dateTime=\'{now}\', action_type=\'{action_type}\', action=\'{action}\'  "
                                   f"WHERE user_id=\'{user_id}\' ")
            else:
                connection.execute(f"INSERT INTO {LAST_ACTION_TABLE_NAME}(user_id, dateTime, action_type, action)  "
                                   f"VALUES( \'{user_id}\', \'{now}\', \'{action_type}\', \'{action}\')")
        except Exception as e:
            debug(e, ERROR)
            transaction.rollback()
        transaction.commit()


# =============================== Ticker request amount ===============================
async def create_request_amount_table(engine=engine):
    with engine.connect() as connection:
        ite = await is_table_exist(REQUEST_AMOUNT_TABLE_NAME, engine)
        if not ite:
            transaction = connection.begin()
            try:
                create_query = f'CREATE TABLE {REQUEST_AMOUNT_TABLE_NAME} ' \
                               f'(user_id  BIGINT NOT NULL, ' \
                               f'paid_amount INT NOT NULL, ' \
                               f'free_amount INT NOT NULL, ' \
                               f'PRIMARY KEY(user_id)' \
                               f')'
                connection.execute(create_query)
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
            transaction.commit()


async def request_amount_lookup(user_id, engine=engine) -> bool:
    with engine.connect() as connection:
        try:
            query_string = f'SELECT * FROM {REQUEST_AMOUNT_TABLE_NAME} ' \
                           f'WHERE user_id = \'{user_id}\' LIMIT 1'
            result = connection.execute(query_string)
            return True if result.rowcount > 0 else False
        except Exception as e:
            debug(e, ERROR)
            return False


async def increment_paid_request_amount(user_id, amount):
    debug(f'user_id:{user_id} amount:{amount}')
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            paid_amount, free_amount = await get_request_amount(user_id)
            now = datetime.datetime.now()
            connection.execute(f"UPDATE {REQUEST_AMOUNT_TABLE_NAME} "
                               f"SET paid_amount=\'{paid_amount+amount}\' "
                               f"WHERE user_id=\'{user_id}\' ")
            transaction.commit()
        except Exception as e:
            debug(e, ERROR)
            transaction.rollback()


async def decrement_paid_request_amount(user_id, amount):
    debug(f'user_id:{user_id} amount:{amount}')
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            paid_amount, free_amount = await get_request_amount(user_id)
            now = datetime.datetime.now()
            connection.execute(f"UPDATE {REQUEST_AMOUNT_TABLE_NAME} "
                               f"SET paid_amount=\'{paid_amount-amount}\' "
                               f"WHERE user_id=\'{user_id}\' ")
            transaction.commit()
        except Exception as e:
            debug(e, ERROR)
            transaction.rollback()


async def increment_free_request_amount(user_id, amount):
    debug(f'user_id:{user_id} amount:{amount}')
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            paid_amount, free_amount = await get_request_amount(user_id)
            now = datetime.datetime.now()
            connection.execute(f"UPDATE {REQUEST_AMOUNT_TABLE_NAME} "
                               f"SET free_amount=\'{free_amount+amount}\' "
                               f"WHERE user_id=\'{user_id}\' ")
            transaction.commit()
        except Exception as e:
            debug(e, ERROR)
            transaction.rollback()


async def decrement_free_request_amount(user_id, amount):
    debug(f'user_id:{user_id} amount:{amount}')
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            paid_amount, free_amount = await get_request_amount(user_id)
            now = datetime.datetime.now()
            connection.execute(f"UPDATE {REQUEST_AMOUNT_TABLE_NAME} "
                               f"SET free_amount=\'{free_amount-amount}\' "
                               f"WHERE user_id=\'{user_id}\' ")
            transaction.commit()
        except Exception as e:
            debug(e, ERROR)
            transaction.rollback()


async def get_request_amount(user_id, engine=engine):
    with engine.connect() as connection:
        try:
            request_amount = (0, 0)
            query_string = f'SELECT paid_amount, free_amount FROM {REQUEST_AMOUNT_TABLE_NAME} ' \
                           f'WHERE user_id = \'{user_id}\' '
            result = connection.execute(query_string)
            if result.rowcount > 0:
                row = result.fetchone()
                request_amount = (row[0], row[1])
            return request_amount
        except Exception as e:
            debug(e, ERROR)
            return request_amount


# =============================== Пришедшие пользователи ===============================
async def create_incoming_users_table(engine=engine):
    with engine.connect() as connection:
        ite = await is_table_exist(INCOMING_USERS_TABLE_NAME, engine)
        if not ite:
            transaction = connection.begin()
            try:
                create_query = f'CREATE TABLE {INCOMING_USERS_TABLE_NAME} ' \
                               f'(user_id  BIGINT NOT NULL, ' \
                               f'income_datetime DATETIME NOT NULL, ' \
                               f'last_request DATETIME, ' \
                               f'PRIMARY KEY(user_id)' \
                               f')'
                connection.execute(create_query)
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
            transaction.commit()


async def incoming_users_lookup(user_id, engine=engine) -> bool:
    with engine.connect() as connection:
        try:
            query_string = f'SELECT * FROM {INCOMING_USERS_TABLE_NAME} ' \
                           f'WHERE user_id = \'{user_id}\' LIMIT 1'
            result = connection.execute(query_string)
            return True if result.rowcount > 0 else False
        except Exception as e:
            debug(e, ERROR)
            return False


async def append_new_user(user_id):
    # Добавляем новго пользователя как в таблицу новопришедших пользователей,
    # так и в таблицу подсчета количества запросов платных - 0, бесплатных сразу даем 25
    with engine.connect() as connection:
        iul = await incoming_users_lookup(user_id)
        if not iul:
            debug(f'----------- Append new user_id:{user_id}')
            transaction = connection.begin()
            try:
                now = datetime.datetime.now()
                connection.execute(f"INSERT INTO {INCOMING_USERS_TABLE_NAME}(user_id, income_datetime)  "
                                   f"VALUES( \'{user_id}\', \'{now}\')")
                connection.execute(f"INSERT INTO {REQUEST_AMOUNT_TABLE_NAME}(user_id, paid_amount, free_amount)  "
                                   f"VALUES( \'{user_id}\', \'0\', \'25\')")
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
            transaction.commit()


async def set_last_request_datetime(user_id):
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            now = datetime.datetime.now()
            connection.execute(f"UPDATE {INCOMING_USERS_TABLE_NAME} "
                               f"SET last_request=\'{now}\' "
                               f"WHERE user_id=\'{user_id}\' ")
        except Exception as e:
            debug(e, ERROR)
            transaction.rollback()
        transaction.commit()


async def get_income_datetime(user_id, engine=engine):
    with engine.connect() as connection:
        try:
            income_datetime = None
            query_string = f'SELECT income_datetime FROM {INCOMING_USERS_TABLE_NAME} ' \
                           f'WHERE user_id = \'{user_id}\' '
            result = connection.execute(query_string)
            if result.rowcount > 0:
                row = result.fetchone()
                income_datetime = datetime.datetime.fromisoformat(str(row[0]))
            return income_datetime
        except Exception as e:
            debug(e, ERROR)
            return income_datetime


async def get_last_request_datetime(user_id, engine=engine):
    with engine.connect() as connection:
        try:
            last_request_datetime = None
            query_string = f'SELECT last_request FROM {INCOMING_USERS_TABLE_NAME} ' \
                           f'WHERE user_id = \'{user_id}\' '
            result = connection.execute(query_string)
            if result.rowcount > 0:
                last_request = str(result.fetchone()[0])
                if last_request != 'NULL':
                    last_request_datetime = datetime.datetime.fromisoformat(last_request)
            return last_request_datetime
        except Exception as e:
            debug(e, ERROR)
            return last_request_datetime


# =============================== Пополнения баланса пользователей ===============================
async def create_payment_history_table(engine=engine):
    with engine.connect() as connection:
        ite = await is_table_exist(PAYMENT_HIST_TABLE_NAME, engine)
        if not ite:
            transaction = connection.begin()
            try:
                create_query = f'CREATE TABLE {PAYMENT_HIST_TABLE_NAME} ' \
                               f'(user_id  BIGINT NOT NULL, ' \
                               f'order_id VARCHAR(20) NOT NULL, ' \
                               f'payment_datetime DATETIME NOT NULL, ' \
                               f'summ DOUBLE NOT NULL, ' \
                               f'PRIMARY KEY(user_id, order_id)' \
                               f')'
                connection.execute(create_query)
            except Exception as e:
                debug(e, ERROR)
                transaction.rollback()
            transaction.commit()


async def save_payment_data(user_id, order_id, summ, engine=engine):
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            now = datetime.datetime.now()
            connection.execute(f"INSERT INTO {PAYMENT_HIST_TABLE_NAME}(user_id, order_id, payment_datetime, summ)  "
                               f"VALUES( \'{user_id}\', \'{order_id}\', \'{now}\', \'{summ}\')")
        except Exception as e:
            debug(e, ERROR)
            transaction.rollback()
        transaction.commit()


