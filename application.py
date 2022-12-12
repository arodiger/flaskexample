from flask import Flask

application = Flask(__name__)

@application.route('/')

def index():
    return " ***** application.py,  Flask Example uploaded to github, Code-pipeline created with auto-update to elastic beanstalk environment redirected to anthonyrodiger.com dns on AWS Network     ******* "

if __name__ == "__main__":
    application.run(debug=False)


