from flask import Flask
from views import views
from flask_restful import Api, Resource, reqparse, abort

application = Flask(__name__)

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


api.add_resource(Video, "/video/<int:video_id>")        #register video class as a resource
api.add_resource(Users, "/Users/<int:user_id>")         #register user class as a resource

if __name__ == "__main__":
    application.run(debug=True)


