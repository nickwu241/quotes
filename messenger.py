import os
import re

from pymessenger.bot import Bot

import quotes

FB_MESSENGER_ACCESS_TOKEN = os.environ['FB_MESSENGER_ACCESS_TOKEN']
FB_MESSENGER_VERIFY_TOKEN = os.environ['FB_MESSENGER_VERIFY_TOKEN']
FB_MESSENGER_BOT = Bot(FB_MESSENGER_ACCESS_TOKEN)

def handle_request(request):
    if request.method == 'GET':
        return handle_get_request(request)
    return handle_post_request(request)

def handle_get_request(request):
    if request.args.get("hub.verify_token") == FB_MESSENGER_VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def handle_post_request(request):
    output = request.get_json()
    for event in output['entry']:
        for message in event['messaging']:
            if not message.get('message'):
                continue
            sid = message['sender']['id']
            text = message['message'].get('text', '')
            if re.search(r'(give me a )?quote(\s+ple+ase|pl(s|z))?', text):
                FB_MESSENGER_BOT.send_text_message(sid, get_random_quote())
    return 'Message Processed'

def get_random_quote():
    q = quotes.random_quote()
    return f"{q['quote']}\n\n- {q['author']}"
