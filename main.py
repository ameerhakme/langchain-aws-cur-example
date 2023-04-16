import json
import os
from typing import Dict

import agent
import config


def handler(event, context): 
    print(f"event is {event}")
    body = json.loads(event["body"])
    
    validate_response = validate_inputs(body)
    if validate_response:
        return validate_response
    
    prompt = body['prompt']
    session_id = body["session_id"]

    print(f"prompt is {prompt}")
    print(f"session_id is {session_id}")
    
    response, session_id = agent.run(
        api_key=config.config.API_KEYS_SECRET_NAME, 
        session_id=session_id, 
        prompt=prompt
    )

    return build_response({
        "response": response,
        "session_id": session_id
    })


def validate_inputs(body: Dict):
    for input_name in ['prompt', 'session_id']:
        if input_name not in body:
            return build_response({
                "status": "error",
                "message": f"{input_name} missing in payload"
            })
    return ""

def build_response(body: Dict):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }

