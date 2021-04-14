from telegram import sql_queries as sql
from project_shared import *


async def db_init_new_tables():
    debug('DB create new tables:')
    ite = await sql.is_table_exist(REQUEST_AMOUNT_TABLE_NAME)
    if not ite:
        debug('>> Try create_request_amount_table')
        await sql.create_request_amount_table()
        debug('## create_request_amount_table complete')
        await init_request_amount_table()

    ite = await sql.is_table_exist(INCOMING_USERS_TABLE_NAME)
    if not ite:
        debug('>> Try create_incoming_users_table')
        await sql.create_incoming_users_table()
        debug('## create_incoming_users_table complete')
        await init_incoming_users_table()

    ite = await sql.is_table_exist(PAYMENT_HIST_TABLE_NAME)
    if not ite:
        debug('>> Try create_payment_history_table')
        await sql.create_payment_history_table()
        debug('## create_payment_history_table complete')
    debug('## DB create new tables complete')


async def init_request_amount_table():
    debug(f'__ init_request_amount_table')
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            connection.execute(f"INSERT INTO {REQUEST_AMOUNT_TABLE_NAME}(user_id, paid_amount, free_amount)  "
                               f"SELECT id, 0, 25 "
                               f"FROM entities")
        except Exception as e:
            debug(e, ERROR)
            transaction.rollback()
        transaction.commit()
    debug(f'__ init_request_amount_table complete')


async def init_incoming_users_table():
    debug(f'__ init_incoming_users_table')
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            now = datetime.datetime.now()
            td = datetime.timedelta(days=4)
            init_date = now - td
            connection.execute(f"INSERT INTO {INCOMING_USERS_TABLE_NAME}(user_id, income_datetime, last_request)  "
                               f"SELECT id, \'{init_date}\', \'{now}\' "
                               f"FROM entities")
        except Exception as e:
            debug(e, ERROR)
            transaction.rollback()
        transaction.commit()
    debug(f'__ init_incoming_users_table complete')
