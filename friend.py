#python modules
import logging
import os
from random import randint

#flask modules
from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement, context, audio, current_stream

#twilo api to notify friend
from twilio.rest import Client
twil_sid = "XX"
twil_tok = "XX"

client = Client(twil_sid, twil_tok)

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    speech_text = 'Whats wrong Victoria?'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

#sends sms
#@ask.intent('TalkIntent')
#def talk_me():
   
 #   cheer = "Let me sing you a song to cheer you up. Excuse my voice, it's been awhile."
  #  sing = 'https://www.dropbox.com/s/da9e42xjbindwpp/golden_girls.mp3?raw=1'
   # return audio(cheer).play(sing, offset=93000)

@ask.intent('SadIntent')
def inspire_me():
    quote_p = render_template('quote'+ str(randint(0,20)))
    did_help ='..Did that help?'
    return question(quote_p + did_help)

@ask.intent('SuccessIntent')
def yes():
    hey = 'I am glad I could help. I am always here for you.'
    return statement(hey) #stop the session

@ask.intent('FailedIntent')
def no():
    sorry = "I\'m sorry to hear that. I can only do so much, I\'m only a robot after all. Should I contact someone?"
    return question(sorry)

@ask.intent('TheEnding')
def human_contact(contact):
    if (contact == 'mom'):
        client.api.account.messages.create(to= "XX",from_="+13213604467 ",body="You need to talk to Victoria")
    elif (contact == 'my best friend'):
        client.api.account.messages.create(to= "XX",from_="+13213604467 ",body="You need to talk to Victoria")
    return statement("Got it.")


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)