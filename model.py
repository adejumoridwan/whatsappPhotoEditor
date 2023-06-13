from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
from dotenv import load_dotenv
import os

load_dotenv()

client = FaunaClient(secret=os.getenv("FAUNA_SECRET"),endpoint="https://db.us.fauna.com/")
#client.query(q.create_collection({"name": "sms"})) 

