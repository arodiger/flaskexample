from flask import Blueprint, render_template
import requests
import confighelper
import mypyLogger
import os

MYPYCONFIG_INI = os.environ.get('MYPYCONFIG_INI', 'PRODUCTION').upper()
# either DEVELOPMENT OR PRODUCTION will be pre-pended to form section title name
webSettings = MYPYCONFIG_INI + "_FLASK_WEBSettings"
# webSettings = "PRODUCTION_FLASK_WEBSettings"

# read in conifgurations.ini file
config = confighelper.read_config()
BASE_URL = config[webSettings]["ini_base_url"]
if (BASE_URL == None):
    mypyLogger.logger.debug("Unable to read base_url from configurations.ini file")    
# BASE_URL = "http://127.0.0.1:5000/"
# BASE_URL = "http://anthonyrodiger.com/"

views = Blueprint(__name__, "views")

@views.route('/')
def home():
    return render_template("home.html", homeParam1="Home Param #1")

@views.route('/one')
def One():
    return render_template("one.html", paramChatHeaderName="WebChat", paramHostNamePort=BASE_URL)

@views.route('/two')
def two():
    return render_template("two.html", pageTwoParam1="Page two param #1")


# make restapi calls during routing to html pages, just for testing
@views.route('/restapiput')
def userRestAPIput():
    response = requests.put(BASE_URL + "video/1" , json={"likes": 10, "name": "tim", "views": 100000} )   
    response = requests.put(BASE_URL + "video/2" , json={"likes": 20, "name": "john", "views": 200000} )   
    response = requests.put(BASE_URL + "video/3" , json={"likes": 30, "name": "george", "views": 300000} )   
    return render_template("RESTapiput.html", restapiputparam1=response.json())

@views.route('/restapiget')
def userRestAPIget():
    response = requests.get(BASE_URL + "video/0")       #give a number outside of current count will return all videos
    return render_template("RESTapiget.html", restapigetparam1=response.json())

@views.route('/restapidelete')
def userRestAPIdelete():
    response = requests.delete(BASE_URL + "video/1")       
    return render_template("RESTapidelete.html", restapideleteparam1="")
