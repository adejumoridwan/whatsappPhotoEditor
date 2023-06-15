from faunadb import query as q
from faunadb.client import FaunaClient
from dotenv import load_dotenv
import os

load_dotenv()

client = FaunaClient(secret=os.getenv("FAUNA_SECRET"),
                     endpoint="https://db.us.fauna.com/")

collection_name = "sms"

# Check if collection exists
try:
    client.query(q.get(q.collection(collection_name)))
    print(f"Collection '{collection_name}' already exists.")
except:
    # Collection doesn't exist, create it
    client.query(q.create_collection({"name": collection_name}))
    print(f"Collection '{collection_name}' created successfully.")
