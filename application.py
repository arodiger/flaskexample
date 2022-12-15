from flask import Flask
from views import views


application = Flask(__name__)

#setup my views.py file to handle the direction of pages
application.register_blueprint(views,url_prefix="/")


if __name__ == "__main__":
    application.run(debug=False)


