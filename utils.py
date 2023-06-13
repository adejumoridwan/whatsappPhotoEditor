import logging
from dotenv import load_dotenv
import os
from twilio.rest import Client
import openai
import requests

load_dotenv()

api_key=os.getenv("API_KEY")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_number = os.getenv('TWILIO_NUMBER')
api_key=os.getenv("API_KEY")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sending message logic through Twilio Messaging API
def send_message(to_number, text):
    try:
        message = client.messages.create(
            from_=twilio_number,
            to=to_number,
            body=text
            )
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")

# SMS Classification
def sms_spam_class(sms):
    API_URL = "https://api-inference.huggingface.co/models/mrm8488/bert-tiny-finetuned-sms-spam-detection"
    headers = {"Authorization": f"Bearer {api_key}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": "f{sms}",
    })

    # Find the scores for 'LABEL_0' and 'LABEL_1'
    label_0_score = None
    label_1_score = None


    for item in output[0]:
        if item['label'] == 'LABEL_0':
            label_0_score = item['score']
        elif item['label'] == 'LABEL_1':
            label_1_score = item['score']

    # Check if 'LABEL_1' score is greater than 'LABEL_0' score
    if label_1_score is not None and label_0_score is not None:
        if label_1_score > label_0_score:
            spam_class = "spam"
        else:
            spam_class = "not spam"
    else:
        spam_class = "Unable to determine spam status."
    
    return spam_class