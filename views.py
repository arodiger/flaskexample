from flask import Blueprint, request, session, render_template, jsonify, make_response
import requests
import confighelper
import mypyLogger
import os
from datetime import datetime, timedelta
import jwt
import json
import base64
import hashlib


MYPYCONFIG_INI = os.environ.get('MYPYCONFIG_INI', 'PRODUCTION').upper()
# either DEVELOPMENT OR PRODUCTION will be pre-pended to form section title name
webSettings = MYPYCONFIG_INI + "_FLASK_WEBSettings"

# read in conifgurations.ini file
config = confighelper.read_config()
BASE_URL = config[webSettings]["ini_base_url"]
if (BASE_URL == None):
    mypyLogger.logger.debug("Unable to read base_url from configurations.ini file")    

# BASE_URL = "http://127.0.0.1:5000/"
# BASE_URL = "http://anthonyrodiger.com/"

views = Blueprint(__name__, "views")

@views.route('/')
def home():
    # insert any code required before loading home/base page
    return render_template("home.html", homeParam1="Home Param #1")

@views.route('/one')
def One():
    # check for registration and/or login
    return render_template("one.html", paramChatHeaderName="Chat", paramHostNamePort=BASE_URL)

@views.route('/two')
def two():
    # check for registration and/or login
    return render_template("two.html", pageTwoParam1="Page two param #1")

@views.route('/loginreg')
def loginreg():
    # check for registration and/or login
    # render loginreg.html and let the javascript perform the login and token verification logic
    return render_template("loginreg.html", paramHostNamePort=BASE_URL)


# "/utils" endpoint handler, authentication and/or registration checks could be enforced here before 
# allowing the execution of the restAPI CRUD calls.
@views.route('/utils')
def utilsRestApiGet():
#     response = requests.put(BASE_URL + "video/1" , json={"likes": 10, "name": "tim", "views": 100000} )   
    response = requests.get(BASE_URL + "utils/8675309")
    return render_template("utils.html", restapigetparam1=response.json())


@views.route('/initcookies', methods=['POST'])
def initcookiesRestApiGet():
    # gather fingerprint info from client header
    # fingerprint algorithim:  md5(Sec-Ch-Ua + User-Agent + Accept-Language )
    try:
        mypyLogger.logger.debug("initCookiesRestApiGet:: Begin function")    
        header_dict = dict(request.headers)

        if request.headers.get('Sec-Ch-Ua'):
            fingerprintSEC = header_dict['Sec-Ch-Ua']
        else:
            fingerprintSEC = ""

        if request.headers.get('User-Agent'):
            fingerprintUSER = header_dict['User-Agent']
        else:
            fingerprintUSER = ""

        if request.headers.get('Accept-Language'):
            fingerprintSERVER = header_dict['Accept-Language']
        else:
            fingerprintSERVER = ""
        
        # fingerprintSEC = header_dict['Sec-Ch-Ua']
        # fingerprintUSER = header_dict['User-Agent']
        # fingerprintSERVER = header_dict['Accept-Language']
        mypyLogger.logger.debug("initCookiesRestApiGet:: fingerprintSEC: " + f"{fingerprintSEC}" )     
        mypyLogger.logger.debug("initCookiesRestApiGet:: fingerprintUSER: " + f"{fingerprintUSER}" )     
        mypyLogger.logger.debug("initCookiesRestApiGet:: fingerprintSERVER: " + f"{fingerprintSERVER}" )     
        
        str2hash = fingerprintSEC + fingerprintUSER + fingerprintSERVER
        mypyLogger.logger.debug("initCookiesRestApiGet:: fingerprint: " + f"{str2hash}" )     

        fingerprintHasObj = hashlib.md5(str2hash.encode())
        requestPayloadFingerprint  = fingerprintHasObj.hexdigest()
        mypyLogger.logger.debug("initCookiesRestApiGet:: requestPayloadFingerprint: " + f"{requestPayloadFingerprint}" )   

        res = make_response()
        lease = 10 * 24 * 60 * 60  # 10 days in seconds

        res.set_cookie( "cookiePayloadFingerprint", value=requestPayloadFingerprint,
            max_age=lease, expires=None, path="/", domain=None, secure=False, httponly=False )

        mypyLogger.logger.debug("initCookiesRestApiGet:: set_cookie complete, now add access-control-allow-origin")    

        res.headers.add("Access-Control-Allow-Origin", "*")
        mypyLogger.logger.debug("initCookiesRestApiGet:: End function")    

    except SyntaxError:
        mypyLogger.logger.debug("initCookiesRestApiGet:: SyntaxError occurred")    
    except TypeError:
        mypyLogger.logger.debug("initCookiesRestApiGet:: TypeError occurred")    
    except NameError:
        mypyLogger.logger.debug("initCookiesRestApiGet:: NameError occurred")    
    except IndexError:
        mypyLogger.logger.debug("initCookiesRestApiGet:: IndexError occurred")    
    except KeyError:
        mypyLogger.logger.debug("initCookiesRestApiGet:: KeyError occurred")    
    except ValueError:
        mypyLogger.logger.debug("initCookiesRestApiGet:: ValueError occurred")    
    except AttributeError:
        mypyLogger.logger.debug("initCookiesRestApiGet:: AttributeError occurred")    
    except IOError:
        mypyLogger.logger.debug("initCookiesRestApiGet:: IOError occurred")    
    except ZeroDivisionError:
        mypyLogger.logger.debug("initCookiesRestApiGet:: ZeroDivisionError occurred")    
    except ImportError:
        mypyLogger.logger.debug("initCookiesRestApiGet:: ImportError occurred")    
    finally:
        return res


# ensure client fingerprint cookie delivered equals dynamically generated client fingerprint cookie
@views.route('/gentoken', methods=['POST'])
def mygentokenRestApiGet():
    # gather fingerprint info from client header
    # fingerprint algorithim:  md5(Sec-Ch-Ua + User-Agent + Accept-Language )
    header_dict = dict(request.headers)
    fingerprintSEC = header_dict['Sec-Ch-Ua']
    fingerprintUSER = header_dict['User-Agent']
    fingerprintSERVER = header_dict['Accept-Language']
    
    str2hash = fingerprintSEC + fingerprintUSER + fingerprintSERVER
    fingerprintHasObj = hashlib.md5(str2hash.encode())
    requestDynamicPayloadFingerprint  = fingerprintHasObj.hexdigest()

    clientCookies = dict(request.cookies)
    cookiePayloadFingerprint = clientCookies['cookiePayloadFingerprint']
    if (requestDynamicPayloadFingerprint == cookiePayloadFingerprint):
        userFingerprintValid = True

        # retrieve from the body data, username password 
        string_data = request.get_data(as_text=True)
        json_data = json.loads(string_data)
        encodedUsername = json_data['username']
        encodedPassword = json_data['password']
        # decode data
        decodedUsername = base64.b64decode(encodedUsername)
        decodedPassword = base64.b64decode(encodedPassword)
        strUsername = str(decodedUsername,'UTF-8')
        strPassword = str(decodedPassword, 'UTF-8')

        # check to ensure they are in the database
        

        # encode to generate token to send back to the client
        # token = jwt.encode({ 'user': 'anthonyrodiger' , 'expiration': str(datetime.utcnow() + timedelta(seconds=60))} , 'a9ea845876aa4e4ea6e65ac196752d69' )
        token = jwt.encode({ 'fingerprint': str2hash ,'password': strPassword , 'user': strUsername , 'expiration': str(datetime.utcnow() + timedelta(seconds=60))} , 'a9ea845876aa4e4ea6e65ac196752d69' )

        res = make_response(jsonify({'token': token}))
        lease = 10 * 24 * 60 * 60  # 10 days in seconds

        res.set_cookie( "refreshToken", value=token,
            max_age=lease, expires=None, path="/", domain=None, secure=False, httponly=False )

        res.set_cookie( "cookiePayloadFingerprint", value=requestDynamicPayloadFingerprint,
            max_age=lease, expires=None, path="/", domain=None, secure=False, httponly=False )

        res.headers.add("Access-Control-Allow-Origin", "*")

        return res          # new
    else:
        mypyLogger.logger.debug("Client Fingerprint doesn't match dynamically generated client fingerprint")    
        return 
   


@views.route('/getitgentoken')
def mygetitgentokenRestApiGet():
    token = jwt.encode({ 'user': 'anthonyrodiger' , 'expiration': str(datetime.utcnow() + timedelta(seconds=60))} , 'a9ea845876aa4e4ea6e65ac196752d69' )
    temp_token = jsonify({'token': token})
    # Enable Access-Control-Allow-Origin
    temp_token.headers.add("Access-Control-Allow-Origin", "*")

    return temp_token


# Login page
@views.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True

        token = jwt.encode({ 'user': request.form['username'] , 'expiration': str(datetime.utcnow() + timedelta(seconds=60))} , views.config['SECRET_KEY'] )
        return jsonify({'token': token})
        # return jsonify({'token': token.decode('utf-8')})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})






#######################################     OLD CODE        #######################################

# headers = CaseInsensitiveDict()
# headers["Accept"] = "application/json"
# headers["Authorization"] = "Bearer {token}"


# resp = requests.get(url, headers=headers)

# print(resp.status_code)
#######################################

# old begin
    # temp_token = jsonify({'token': token})
    # print("@@@@@@@@@@@@@  gentoken POST called @@@@@@@@@@@@@")
    # temp_token.headers.add("Access-Control-Allow-Origin", "*")
    # temp_token.set_cookie("testcookiekey", "testcookievalue")
    # # temp_token.set_cookie( 'refreshToken',
    # #     value=token.encode('utf-8'),
    # #     max_age=500,
    # #     expires=None,
    # #     secure=False
    # # )
# old end

#######################################

# class MyGenTokenClass(Resource):
#     def get(self, mygentoken_id):
#         data = request.json()
#         if request.form['username'] and request.form['password'] == '123456':
#             token = jwt.encode({ 'user': request.form['username'] , 'expiration': str(datetime.utcnow() + timedelta(seconds=60))} , app.config['SECRET_KEY'] )
#             return jsonify({'token': token})
#             # return jsonify({'token': token.decode('utf-8')})
#         else:
#             return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})
#######################################



# # make restapi calls during routing to html pages, just for testing
# @views.route('/restapiput')
# def userRestAPIput():
#     response = requests.put(BASE_URL + "video/1" , json={"likes": 10, "name": "tim", "views": 100000} )   
#     response = requests.put(BASE_URL + "video/2" , json={"likes": 20, "name": "john", "views": 200000} )   
#     response = requests.put(BASE_URL + "video/3" , json={"likes": 30, "name": "george", "views": 300000} )   
#     return render_template("RESTapiput.html", restapiputparam1=response.json())

# @views.route('/restapiget')
# def userRestAPIget():
#     response = requests.get(BASE_URL + "video/0")       #give a number outside of current count will return all videos
#     return render_template("RESTapiget.html", restapigetparam1=response.json())

# @views.route('/restapidelete')
# def userRestAPIdelete():
#     response = requests.delete(BASE_URL + "video/1")       
#     return render_template("RESTapidelete.html", restapideleteparam1="")
#######################################     OLD CODE        #######################################
