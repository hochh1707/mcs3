import sys
import time
import random
import requests
from classProxyStuff import classProxyStuff
from classScraper import classScraper
from classLogStuff import classLogStuff
from flask import Flask


mode = "p"

application = Flask(__name__)

@application.route('/')
def home():
    return "home"

@application.route('/scraper')
def scraper():
    cs = classScraper()
    cs.scraperMain(mode)
    return "aaa1"

@application.route('/dashboard')
def dashboard():
    ttt = ""
    f1 = open("./logs/dashboard.txt")
    for i in f1:
        ttt += "<h2>" + i + "</h2>"
    return ttt

if __name__ == "__main__":
    application.run()
    