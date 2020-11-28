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
