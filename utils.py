from dotenv import load_dotenv
import os
import requests
from twilio.rest import Client


load_dotenv()

api_key=os.getenv("HUGGING_API_KEY")

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
            spam_class = "ham"
    else:
        spam_class = "Unable to determine spam status."
    
    return spam_class