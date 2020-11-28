
async def user_search(identifier, connection=None):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM  entities WHERE id = %s", [identifier])
        row = cursor.fetchone()
    return row


async def db_save_lang(value, identifier, connection=None):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE entities SET profile_lang = %s WHERE id = %s",
                       [value, identifier])


async def db_save_referral(value, identifier, connection=None):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE entities SET referral = %s WHERE id = %s",
                       [value, identifier])