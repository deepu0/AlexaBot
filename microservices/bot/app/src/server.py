from src import app
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
import random


ask = Ask(app, "/yoda_quotes")

def getYodaQuote():
	url = "http://data.hasura/v1/query"
	headers = {
		"Content-Type": "application/json",
        "X-Hasura-User-Id": "1",
        "X-Hasura-Role": "admin"
	}
	body = {
	    "type": "run_sql",
	    "args": {
	        "sql": "SELECT quote FROM yoda_quotes ORDER BY RANDOM() limit 1;"
	    }
	}
	
	response = requests.request("POST", url, data=json.dumps(body), headers=headers)
	respObj = response.json()
	print (respObj)
	return (respObj["result"][1][0])


@app.route('/')
def homepage():
    return "Alexa skill is running."

@ask.launch
def startSkill():
    quote = getYodaQuote()
    response = quote + '...... mmmmmmm ......... Do you want more?'
    return question(response)

@ask.intent("YesIntent")
def shareQuote():
    quote = getYodaQuote()
    response = quote + '...... mmmmmmm ......... Do you want more?'
    return question(response)

@ask.intent("HelpIntent")
def helpQuote():
    response = 'This Skill provides you the best motivational quotes. Do you want to get your daily motivation ?'
    return question(response)

@ask.intent("StopIntent")
def noIntent():
    response = 'Goodbye!'
    return statement(response) 

@ask.intent("CancelIntent")
def noIntent():
    response = 'Goodbye!'
    return statement(response)        

@ask.intent("NoIntent")
def noIntent():
    byeText = 'Lol... OK... Bye'
    return statement(byeText)
