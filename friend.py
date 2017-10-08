import logging
from random import randint
import os

from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    speech_text = 'Whats wrong Victoria'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


#@ask.intent('HelloWorldIntent')
#def hello_world():
 #   speech_text = 'Hello little andrea'
  #  return statement(speech_text).simple_card('HelloWorld', speech_text)

@ask.intent('InspireIntent')
def inspire_me():
    quote_p = render_template('quote'+ str(randint(0,20)))
    return statement(quote_p)


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