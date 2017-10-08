import logging
import os
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
   speech_text = render_template('initial_question'+str(randint(3,3)))
   return question(speech_text)

@ask.intent('InspireIntent')
def inspire_me():
   number = str(randint(1,20))
   speech_text = str(render_template('quote'+number)) + '...' + 'did that help?'
   print ('quote'+number)
   return question(speech_text)

@ask.intent('QuoteFailed')
def next_question():
   speech_text = "Okay. How does getting lit sounds  right now?"
   return question(speech_text)


@ask.session_ended
def session_ended():
   return "{}", 200


if __name__ == '__main__':
   if 'ASK_VERIFY_REQUESTS' in os.environ:
       verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
       if verify == 'false':
           app.config['ASK_VERIFY_REQUESTS'] = False
   app.run(debug=True)