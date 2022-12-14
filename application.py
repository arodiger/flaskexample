from flask import Flask
from views import views


application = Flask(__name__)

#setup my views.py file to handle the direction of pages
application.register_blueprint(views,url_prefix="/")


# @application.route('/')
# def index():
#     return " ***** application.py,  Flask Example uploaded to github, Code-pipeline created with auto-update to elastic beanstalk environment redirected to anthonyrodiger.com dns on AWS Network     ******* "

if __name__ == "__main__":
    application.run(debug=False)


