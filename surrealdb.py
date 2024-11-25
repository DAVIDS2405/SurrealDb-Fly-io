from fastapi import HTTPException, status
from surrealdb import Surreal
from config.index import settings
from logger.logger import logger


url_db = settings.URL_DB_SURREAL
username_db = settings.USER_DB_SURREAL
password_db = settings.PASSWORD_DB_SURREAL
namespace_db = settings.NAMESPACE_DB_SURREAL
database_db = settings.DATABASE_DB_SURREAL


async def Connection():
    global db_connection
    try:
        # Whit SurrealHTTP (Problems in the present version)

        # conn = SurrealHTTP(
        #     url="http://localhost:8080",
        #     namespace="test",
        #     database="test",
        #     username="root",
        #     password="root"
        # )
        # print(await conn.select('users'))
        # return conn

        # Whit Surreal  use ws in local and wss to prod
        conn = Surreal(
            url_db
        )
        await conn.connect()
        await conn.signin({"user": username_db, "pass": password_db})
        await conn.use(namespace=namespace_db, database=database_db)
        db_connection = conn
        return conn

    except Exception as e:

        logger.error(f'No funciono la base de datos {e}')

        raise RuntimeError('Error to connect whit the database')


async def Disconnect():
    global db_connection

    if db_connection:
        await db_connection.close()
        logger.info("Conexión a la base de datos cerrada.")
