# -*- coding: utf-8 -*-
import os
import re
import gemini
import logging
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# SMS endpoint using Twilio's TwiML
@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming SMS with a friendly message."""
    msg = request.form.get('Body', '')
    resp = MessagingResponse()
    
    try:
        if msg:
            response_text = gemini.send_message(msg)
        else:
            response_text = "No message received."
        resp.message(response_text)
    except Exception as e:
        logger.error(f"An error occurred while processing SMS: {e}")
        resp.message("There was an error processing your message.")
    
    return str(resp)

# Route for testing the gemini.py file
'''
 make an API call to this route like this
{
    "query" : "What is java? "
}
'''
@app.route('/testing', methods=['POST'])
def testing():
    if request.is_json:
        data = request.get_json()
        query = data.get("query", "")
        try:
            response_text = gemini.send_message(query)
            return jsonify({'status': 'ok', 'response': response_text})
        except Exception as e:
            logger.error(f"An error occurred while processing updates: {e}")
            return jsonify({'status': 'error', 'message': str(e)})
    else:
        return jsonify({'status': 'error', 'message': 'Request must be JSON'})

# Route for starting the application
@app.route('/', methods=['GET'])
def start():
    return jsonify({'status': 'ok', 'message': 'Application started'})

if __name__ == '__main__':
    app.run()
