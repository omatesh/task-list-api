from flask import abort, make_response
import requests
from ..db import db
import os

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"details": "Invalid data"}
        abort(make_response(response , 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)
    
    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))
    
    return model


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
        
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

def send_slack_message(task_title):
    slack_token = os.environ.get("SLACK_TOKEN")  # Get token from environment variables
    slack_url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {slack_token}"}
    slack_channel = os.environ.get("SLACK_CHANNEL")  
    data = {
        "channel": slack_channel,  # Channel name in Slack
        "text": f"Someone just completed the task {task_title}"  # Message text
    }

    response = requests.post(slack_url, headers=headers, json=data)
    return response.json()["ok"]