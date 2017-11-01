import os
from flask import Flask, request, Response
from slackclient import SlackClient

app = Flask(__name__)

#SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')
#SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)
SLACK_WEBHOOK_SECRET =''
#SLACK_TOKEN = 'xoxp-265846052229-265846052341-267092027495-56cf8b7320cb74a8b0623b564a9a0c96'

SLACK_TOKEN = 'xoxb-265640319955-k1v8Ve0ulcb5kdSyi5ILARxq'

slack_client = SlackClient(SLACK_TOKEN)
CHANNEL_ID = None



@app.route('/slack', methods=['POST'])
def inbound():
    print(request.form.get('token'))
    if True:
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')
	
	#for key, value in request.form.iteritems():
        #    print key
	if channel == 'general':
		if ('Hey Haribot!' in text) and  (username != 'slackbot'):
			send_message(CHANNEL_ID, 'Thanks ' + username + '! We have received your submission BEEP BOOP BEEEP!')
        		inbound_message = "SUBMISSION BY " + username + ": " +  text
        		print(inbound_message)


			user_id = request.form.get('user_id')
			fh = open("./submissions.txt", "a")
			fh.write(user_id + "\t" + username + "\t" + text + "\n")
			fh.close()
			
			#slack_client.api_call("conversations.create",name="voting",is_private=True)
			#slack_client.api_call("conversations.open",users=[user_id])
			#slack_client.api_call("chat.postMessage",channel=user_id,text="Hello from Python! :tada:", username='haribot')
    return Response(), 200


@app.route('/', methods=['GET'])
def test():
    return Response('It works!')


##### HELPER METHODS #####

def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call['ok']:
        return channels_call['channels']
    return None

def channel_info(channel_id):
    channel_info = slack_client.api_call("channels.info", channel=channel_id)
    if channel_info:
        return channel_info['channel']
    return None

def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='haribot',
        icon_emoji=':robot_face:'
    )


##### MAIN #####

if __name__ == "__main__":
    channels = list_channels()
    for channel in channels:
	if channel['name'] == 'general':
	    send_message(channel['id'], 'Hello Students! My name is Haribot. Today, I will be posting an open question for you to think about. You will have 24 hours to think of a solution and post a 2-3 sentence proposal. After the 24 hour proposal period, users will then get to vote on the best proposals! Each student will receive extra credit points relative to the number of votes they receive for up to 5 points!.   \n Todays Question: What is a good way to encourage participation in group slack channels using incentive compatible mechanisms?.\n You have 24 hours to post your answer on this slack channel. Ping @haribot and begin your submission with \' Hey Haribot! \' in order to enter a submission. We will describe voting procedure after the proposal window has closed. ')
	    CHANNEL_ID = channel['id']
	break
    app.run(debug=True)




















