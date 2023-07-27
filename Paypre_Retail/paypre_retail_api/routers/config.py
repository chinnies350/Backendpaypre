import aioodbc
import asyncio
from aioodbc.cursor import Cursor
from concurrent.futures import ThreadPoolExecutor
from pyodbc import OperationalError
from starlette.exceptions import HTTPException
from starlette.status import HTTP_502_BAD_GATEWAY
from asyncio import AbstractEventLoop

loop: AbstractEventLoop = asyncio.get_event_loop()


async def get_cursor() -> Cursor:
    dsn= r'Driver={ODBC Driver 17 for SQL Server};Server={192.168.1.221};Database={Paypre_Retail};UID={sqldeveloper};PWD={SqlDeveloper$};MARS_Connection=yes;APP=yourapp'
    try:
        async with aioodbc.connect(dsn=dsn, loop=loop, executor=ThreadPoolExecutor(max_workers=50)) as conn:
            async with conn.cursor() as cur:
                yield cur
    except OperationalError:
        raise HTTPException(status_code=HTTP_502_BAD_GATEWAY,
                                detail='DB connection failed')




