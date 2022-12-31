from flask import Flask
from views import views
from flask_restful import Api, Resource, reqparse, abort
from flask_socketio import SocketIO, send


application = Flask(__name__)
socketio = SocketIO(application,logger=False, engineio_logger=False, cors_allowed_origins="*")  #setup socket

application.register_blueprint(views,url_prefix="/")    #setup my views.py file to handle the direction of pages
api = Api(application)                                  #wrap our application with the api

video_put_args = reqparse.RequestParser()               #utilize RequestParser class which will parse out data

video_put_args.add_argument('name', type=str, help='Name of video is required', required=True)
video_put_args.add_argument("views", type=int, help="Views of video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on video is required", required=True)

videos = {}

def abortIfVideoIdDoesntExist(video_id):
    if video_id not in videos:
        abort(404, message="Video not valid")

def abortIfVideoExists(video_id):
    if video_id in videos: 
        abort(409, message="Video already exists with that id")

class Users(Resource):
    def get(self, user_id):
        print("inside get of tempUser")
        return "", 200


class Video(Resource):                                  #create resource class and methods that will satisfy api calls
    def get(self, video_id):
        if video_id not in videos:
            return videos                               #return entire dictionary
        else:
            return videos[video_id]

    def put(self, video_id):
        abortIfVideoExists(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201

    def delete(self, video_id):                         #modified to delete all
        abortIfVideoIdDoesntExist(video_id)
        videos.clear()                                  #modified to delete all
        # del videos[video_id]
        return "", 204

# Flask-SocketIO, registering handlers for events
# socket handler accepts message and broadcast out to all connected users
# this handler uses string messages
@socketio.on('message')
def handle_message(message):
    print("SERVER Received message: " + message)
    if message != "User connected!":
        send(message, broadcast=True)

# this handler uses JSON data
@socketio.on('json')
def handle_json(json):
    print("SERVER Received JSON message: " + str(json))

# registering connect handler 
@socketio.on('connect')
def test_connect(auth):
    send('Client Connected', broadcast=True)
    print(f"SERVER Client connected message: {auth}")

# registering disconnect handler 
@socketio.on('disconnect')
def test_disconnect():
    send('Client disconnected', broadcast=True)
    print("SERVER Client disconnected message: ")


api.add_resource(Video, "/video/<int:video_id>")        #register video class as a resource
api.add_resource(Users, "/Users/<int:user_id>")         #register user class as a resource

if __name__ == "__main__":
    socketio.run(application,host="localhost", port=5000, debug=False, log_output=False)
    application.run(debug=False)


