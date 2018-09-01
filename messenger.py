import os

from pymessenger.bot import Bot

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
    print('handling post request')
    output = request.get_json()
    for event in output['entry']:
        for message in event['messaging']:
            if not message.get('message'):
                continue
            recipient_id = message['sender']['id']
            if message['message'].get('text'):
                FB_MESSENGER_BOT.send_text_message(recipient_id, 'Hello!')
            if message['message'].get('attachments'):
                FB_MESSENGER_BOT.send_text_message(recipient_id, 'Hello!')
    return 'Message Processed'
