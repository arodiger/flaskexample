from flask import Flask, request
from views import views
from flask_restful import Api, Resource, reqparse, abort
from flask_socketio import SocketIO, send, join_room, leave_room
from flask_session import Session


application = Flask(__name__)
Session(application)                                    # invoke server side sessions for our chat application, manage_session=False
socketio = SocketIO(application, manage_session=False, logger=False, engineio_logger=False, cors_allowed_origins="*")  #setup socket

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

chatRoomSessionList = []        # [ {chatRoomSession} ]
chatRoomSession = {}            # {"sessionid":"" , "username": ""}
currentLoggedInSessions = []    #[sessionid, sessionid]

chatHistory = []                # [ {webChat}, {webChat}]
webChat = {}                    # {"username":"", "message":"", "timestamp":"", "loadhistory":""}

usernameMessage = []
LOADHISTORY = "LOADHISTORY"
# Flask-SocketIO, registering handlers for events
# socket handler accepts message and broadcast out to all connected users
# maybe i should ensure a user is part of a "room" and logged in before sending him messages YES
# this would allow for messages to come and go, however only update application if logged into room
# since socket connections can persist for sometime need to incorporate the "room" logic
@socketio.on('message')
def handle_message(message):
    global chatRoomSession
    usernameMessage = message.split(":")
    webChat = {"username": usernameMessage[0], "message": usernameMessage[1], "timestamp":usernameMessage[2], "loadhistory": usernameMessage[3]}
    clientSession = request.sid
    if clientSession not in currentLoggedInSessions:
        currentLoggedInSessions.append(clientSession)
    print(webChat)
    if (webChat["loadhistory"] == LOADHISTORY ):           #client request to load history
        for entry in chatHistory:
            msg = entry["username"] + ":" + entry["message"] + ":" + entry["timestamp"]
            send(msg, to=clientSession)                 #only send history to client requesting

        join_room('WebChatRoom')
        chatRoomSession = { "sessionid": clientSession, "username": webChat["username"] }
        chatRoomSessionList.append(chatRoomSession)

        send(f'{webChat["username"]} : has entered the chat. :',to='WebChatRoom', include_self=False)
    else:
        if ( len(webChat["message"]) > 0):              #only send msg if there is data
            send(message, broadcast=True)
            chatHistory.append(webChat)
            print(chatHistory)


# # this handler uses JSON data
@socketio.on('json')
def handle_json(json):
    print("***************************************************")
    print("SERVER Received JSON message: " + str(json))
    print("***************************************************")

# registering connect handler 
# @socketio.on('connect')
# def test_connect(auth):
#    print(f"SERVER Client connected message: {auth}")

# registering disconnect handler 
# remove the client from the client session list and from the chat room session dictionary
# implement leave_room here, then we can add room to send(message,room)
# send message to remaining clients who left the chat
@socketio.on('disconnect')
def test_disconnect():
    clientSession = request.sid
    if clientSession in currentLoggedInSessions:
        currentLoggedInSessions.remove(clientSession)           #removed from session list

    for chatRoomDict in chatRoomSessionList:
        if chatRoomDict["sessionid"] == clientSession:
            chatRoomSessionList.remove(chatRoomDict)            #removed from chat room session dictionary
            send(f'{chatRoomDict["username"]} : has left the chat:',skip_sid=clientSession, broadcast=True)
            leave_room("WebChatRoom", clientSession)



# @socketio.on('join')
# def on_join(data):
#     send('someone has entered the room.')


api.add_resource(Video, "/video/<int:video_id>")        #register video class as a resource
api.add_resource(Users, "/Users/<int:user_id>")         #register user class as a resource

if __name__ == "__main__":
    socketio.run(application,host="localhost", port=5000, debug=False, log_output=False)
    application.run(debug=False)


