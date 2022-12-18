from flask import Blueprint, render_template
import requests

#BASE = "http://127.0.0.1:5000/"
BASE = "http://anthonyrodiger.com/"

views = Blueprint(__name__, "views")

@views.route('/')
def home():
    return render_template("home.html", homeParam1="Home Param #1")

@views.route('/one')
def One():
    return render_template("one.html", pageOneParam1="Page one param #1")

@views.route('/two')
def two():
    return render_template("two.html", pageTwoParam1="Page two param #1")


@views.route('/restapiput')
def userRestAPIput():
    response = requests.put(BASE + "video/1" , json={"likes": 10, "name": "tim", "views": 100000} )   
    print(response.json())
    response = requests.put(BASE + "video/2" , json={"likes": 20, "name": "john", "views": 200000} )   
    print(response.json())
    response = requests.put(BASE + "video/3" , json={"likes": 30, "name": "george", "views": 300000} )   
    print(response.json())
    return render_template("RESTapiput.html", restapiputparam1=response.json())


@views.route('/restapiget')
def userRestAPIget():
    response = requests.get(BASE + "video/0")       #give a number outside of current count will return all videos
    print(response.json())
    return render_template("RESTapiget.html", restapigetparam1=response.json())

