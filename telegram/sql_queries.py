async def user_search(identifier, engine=None):
    with engine.connect() as connection:
        result = connection.execute("SELECT * FROM  entities WHERE id = %s", [identifier])
        return result.cursor.fetchone()


async def db_save_lang(value, identifier, engine=None):
    with engine.connect() as connection:
        result = connection.execute("UPDATE entities SET profile_lang = %s WHERE id = %s", [value, identifier])
        return result.cursor.fetchone()


async def db_save_referral(value, identifier, engine=None):
    with engine.connect() as connection:
        connection.execute("UPDATE entities SET referral = %s WHERE id = %s", [value, identifier])
        connection.execute("commit")


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
        connection.execute("DELETE from payment_message_hist WHERE id = %s", order_id)
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
