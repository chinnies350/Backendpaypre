# from sqlalchemy import create_engine
import asyncio
import aioodbc
from aioodbc.cursor import Cursor
from pymongo  import MongoClient
from concurrent.futures import ThreadPoolExecutor
from starlette.status import HTTP_502_BAD_GATEWAY
from starlette.exceptions import HTTPException
from pyodbc import OperationalError
from asyncio import AbstractEventLoop
import redis

# mssql asynchronous connection
loop = asyncio.get_event_loop()

# REDIS_HOST = 'redis'
REDIS_HOST = '192.168.1.16'
REDIS_PORT = 6379
REDIS_DB = 0

# RABBITMQ_HOST = 'myrabbit'
RABBITMQ_HOST = '192.168.1.16'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'admin'
RABBITMQ_PASSWORD = 'Prematix@123'

redis_client=redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# client = MongoClient("mongodb://admin:Prematix%40123@mongodb_server:27017/?authMechanism=DEFAULT")
client = MongoClient("mongodb://admin:Prematix%40123@192.168.1.16:7017/?authMechanism=DEFAULT")

db = client['paypre']

# Get a collection for logs
logs_collection = db['logs']

SMS_URL = "http://smsstreet.in/websms/sendsms.aspx"
SMS_API_SAFETY_KEY = "smart-parking"


# engine = create_engine('mssql+pyodbc://paypreuser:password123@192.168.1.173/smart_parking?driver=ODBC+Driver+17+for+SQL+Server&Mars_Connection=Yes')

loop: AbstractEventLoop = asyncio.get_event_loop()

async def get_cursor() -> Cursor:
    dsn = r'Driver={ODBC Driver 17 for SQL Server};Server={192.168.1.221};Database={PayPre_Common_FrameWork};UID={appUser};PWD={AppUser@221#$*};MARS_Connection=yes;APP=yourapp'


    try:
        async with aioodbc.connect(dsn=dsn, loop=loop, executor= ThreadPoolExecutor(max_workers=50)) as conn:
            async with conn.cursor() as cur:
                yield cur
    except OperationalError:
        raise HTTPException(status_code=HTTP_502_BAD_GATEWAY,
                                detail='DB connectivity failed')






