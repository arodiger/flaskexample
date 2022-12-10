from flask import Flask

application = Flask(__name__)

@application.route('/')

def index():
    return " *****   APPLICATION.PY    Testing Flask Example on AWS Network ******* "

if __name__ == "__main__":
    application.run(debug=False)


