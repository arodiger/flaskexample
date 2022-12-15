from flask import Blueprint, render_template

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

