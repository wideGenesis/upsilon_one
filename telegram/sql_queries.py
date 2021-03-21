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


async def is_table_exist(table_name, engine=None) -> bool:
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


def create_donate_data_table(engine=None):
    with engine.connect() as connection:
        if not is_table_exist(DONATE_DATA_TABLE_NAME):
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


def save_donate_data(sender_id, summa):
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            now = datetime.datetime.now()
            connection.execute("INSERT INTO donate_data(dateTime, user_id, sum) "
                               "VALUES( %s, %s, %s, %s )", [now, sender_id, summa])
        except Exception as e:
            debug(e, ERROR)
            transaction.rollback()
        transaction.commit()
