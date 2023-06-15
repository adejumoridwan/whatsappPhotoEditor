from fastapi import FastAPI, Form, Request
from utils import sms_spam_class
from dotenv import load_dotenv
import os
from faunadb import query as q
from model import client

load_dotenv()

app = FastAPI(debug=True)

@app.post("/sms")
async def reply(request: Request):
    form_data = await request.form()
    MessageSid = form_data["MessageSid"]
    AccountSid = form_data["AccountSid"]
    From = form_data["From"]
    Body = form_data["Body"]
    To = form_data["To"]

    spam_class = sms_spam_class(Body)
    response = client.query(q.create(q.collection("sms"), {"data": {
        "MessageSid": MessageSid,
        "AccountSid": AccountSid,
        "From": From,
        "Body": Body,
        "To": To,
        "spam_classification": spam_class
    }}))


    return ""