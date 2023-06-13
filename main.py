from fastapi import FastAPI, Form, File, UploadFile
import requests
from utils import send_message, sms_spam_class
from dotenv import load_dotenv
import os
import json
import openai
from twilio.twiml.messaging_response import MessagingResponse
from pydantic import BaseModel
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
from model import client


load_dotenv()

app = FastAPI(debug=True)
to_number = os.getenv("TO_NUMBER")
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.post("/sms")
def reply(sms: str = Form(...)):
    message = sms_spam_class(sms)
    response = client.query(q.create(q.collection("sms"), {"data": {
        "sender_number": to_number,
        "sms": sms,
        "spam_classification": message
    }}))
    return ""