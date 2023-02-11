from flask import Flask, request
from views import views
from flask_restful import Api, Resource, reqparse, abort
from flask_socketio import SocketIO, send, join_room, leave_room
from flask_session import Session
import json
import mypyLogger

from postDB import Database
import confighelper
 
# read in configurations.ini file
config = confighelper.read_config()
config_table_name = config["NewDatabaseInitSettings"]["ini_table_name"]

# get connection to postgres database
webchatDB = Database()
webchatDB.initialize()

application = Flask(__name__)                           # AWS doesn't like app.py, utilize different name
application.config['SECRET_KEY'] = 'a9ea845876aa4e4ea6e65ac196752d69'
Session(application)                                    # invoke server side sessions for our chat application, manage_session=False
socketio = SocketIO(application, manage_session=False, logger=False, engineio_logger=False, cors_allowed_origins="*")  #setup socket

application.register_blueprint(views,url_prefix="/")    #setup my views.py file to handle the direction of pages
api = Api(application)                                  #wrap our application with the api

video_put_args = reqparse.RequestParser()               #utilize RequestParser class which will parse out data

video_put_args.add_argument('name', type=str, help='Name of video is required', required=True)
video_put_args.add_argument("views", type=int, help="Views of video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on video is required", required=True)

# create login and/or registration class and methods that will satisfy api calls
# if valid username & password, then return jwt token
class LoginReg(Resource):
    def post(self):
        title = request.json['username']
        content = request.json['password']
        temp = {'loginreg' : 'POST', 'content' : 'POST content' }
        return temp

    def get(self):
        temp = {'loginreg' : 'GET', 'content' : 'GET content' }
        return temp


# create resource class and methods that will satisfy api calls
class ChatUtils(Resource):
    def post(self):
        title = request.json['title']
        content = request.json['content']
        temp = {'chat' : 'POST', 'content' : 'POST content' }
        return temp

    def get(self):
        temp = {'chat' : 'GET', 'content' : 'GET content' }
        return temp

    def delete(self):                         #modified to delete all
        selectAllQuery = "TRUNCATE TABLE public.webchat"
        queryResults = webchatDB.select_webchat_history(query=selectAllQuery)
        #commit the transaction
        webchatDB.commit()
        return "", 204


# create resource class and methods that will satisfy api calls
class DebugUtils(Resource):
    def post(self):
        title = request.json['title']
        content = request.json['content']
        temp = {'debug' : 'POST', 'content' : 'POST content' }
        return temp

    def get(self):
        temp = {'debug' : 'GET', 'content' : 'GET content' }
        return temp

# create resource class and methods that will satisfy api calls
class Utils(Resource):
    def get(self, utils_id):
        selectAllQuery = "SELECT * FROM public.webchat"
        qResults = webchatDB.select_webchat_history(query=selectAllQuery)
        
        
        webchatDB.commit()
        return qResults


chatRoomSessionList = []        # [ {chatRoomSession} ]
chatRoomSession = {}            # {"sessionid":"" , "username": ""}
currentLoggedInSessions = []    #[sessionid, sessionid]

chatHistory = []                # [ {clientData}, {clientData}]
clientData = {}                    # {"username":"", "message":"", "time_stamp":"", "loadhistory":""}

tempDict = {}

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
    clientData = json.loads(message)
    clientSession = request.sid
    if clientSession not in currentLoggedInSessions:
        currentLoggedInSessions.append(clientSession)
    mypyLogger.logger.debug(clientData)
    if (clientData["loadhistory"] == LOADHISTORY ):           #client request to load history
        # query db for chatHistory
        selectAllQuery = "SELECT * FROM public.webchat"
        queryResults = webchatDB.select_webchat_history(query=selectAllQuery)
        #commit the transaction
        webchatDB.commit()
        for entry in queryResults:
            testJson = json.dumps(entry)
            send(testJson, to=clientSession)                 #only send history to client requesting

        join_room('WebChatRoom')
        chatRoomSession = { "sessionid": clientSession, "username": clientData["username"] }
        chatRoomSessionList.append(chatRoomSession)

        # send(f'{clientData["username"]} : has entered the chat. :',to='WebChatRoom', include_self=False)
        clientData["message"] = "has entered the chat"
        joinChatMessage = json.dumps(clientData)
        send(joinChatMessage,to='WebChatRoom', include_self=False)
    else:
        if ( len(clientData["message"]) > 0):              #only send msg if there is data
            send(message, broadcast=True)
            chatHistory.append(clientData)
            mypyLogger.logger.debug(chatHistory)
            # ##########insert msg into db POSTGRESDB INSERT##########
            webchatDB.insert_into_db(clientData,tablename=config_table_name)
            webchatDB.commit()            
            # ##########insert msg into db POSTGRESDB INSERT##########


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
            send(json.dumps({"username": chatRoomDict["username"], "message": "has left the chat"}), skip_sid=clientSession, broadcast=True)
            leave_room("WebChatRoom", clientSession)



# registering the classes to be the restAPI CRUD handlers for requested endpoints
api.add_resource(Utils, "/utils/<int:utils_id>")                # /utils/1, endpoint which requires int to be passes
api.add_resource(ChatUtils, "/ChatAdmin", "/chatadmin")         # /ChatAdmin, /chatadmin is the endpoints 
api.add_resource(DebugUtils, "/DebugAdmin", "/debugadmin")      # /DebugAdmin, /debugadmin is the endpoints
api.add_resource(LoginReg, "/loginreg")

if __name__ == "__main__":
    socketio.run(application,host="localhost", port=5000, debug=False, log_output=False)
    application.run(debug=False)




#######################################     OLD CODE        #######################################
# videos = {}

# def abortIfVideoIdDoesntExist(video_id):
#     if video_id not in videos:
#         abort(404, message="Video not valid")

# def abortIfVideoExists(video_id):
#     if video_id in videos: 
#         abort(409, message="Video already exists with that id")

# class Users(Resource):
#     def get(self, user_id):
#         mypyLogger.logger.debug("inside get of tempUser")
#         return "", 200

# # create resource class and methods that will satisfy api calls
# class Video(Resource):          
#     def get(self, video_id):
#         selectAllQuery = "SELECT * FROM public.webchat"
#         queryResults = webchatDB.select_webchat_history(query=selectAllQuery)
#         #commit the transaction
#         webchatDB.commit()
#         return queryResults

#     def put(self, video_id):
#         abortIfVideoExists(video_id)
#         args = video_put_args.parse_args()
#         videos[video_id] = args
#         return videos[video_id], 201

#     def delete(self, video_id):                         #modified to delete all
#         selectAllQuery = "TRUNCATE TABLE public.webchat"
#         queryResults = webchatDB.select_webchat_history(query=selectAllQuery)
#         #commit the transaction
#         webchatDB.commit()
#         return "", 204

# api.add_resource(Video, "/video/<int:video_id>")        #register video class as a resource
# api.add_resource(Users, "/Users/<int:user_id>")         #register user class as a resource
#register Utils class as a resource


# @socketio.on('join')
# def on_join(data):
#     send('someone has entered the room.')

# # this handler uses JSON data
# @socketio.on('json')
# def handle_json(json):
#     mypyLogger.logger.debug("***************************************************")
#     mypyLogger.logger.debug("SERVER Received JSON message: " + str(json))
#     mypyLogger.logger.debug("***************************************************")

# registering connect handler 
# @socketio.on('connect')
# def test_connect(auth):
#    mypyLogger.logger.debug(f"SERVER Client connected message: {auth}")
#    print(f"SERVER Client connected message: {auth}")


#######################################     OLD CODE        #######################################


