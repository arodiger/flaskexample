#       set environment variables to run flask
# >set FLASK_APP=application.py
# >$env:FLASK_APP="application.py"
# >flask run

#       requirements.txt needs to be updated before 
#       pushing to production
# >pip freeze > requirements.txt

#       SETUP AND PUSH YOUR CODE TO GETHUB VIA COMMANDLINE
# > git init
#       make sure you have a .gitignore file saved into your project directory
#       this will ensure unneeded files do not get copied to github 
# > git add .
# > git commit -m 'init or any info to describe this version of code changes'

#       goto github and create new repository "projectName" 
#       "push an existing repository from command line"
#       you can copy the commands and execute from command line
# > git remote add origin https://github.com/xxx/flaskexample.git
# > git branch -M main 
# > git push -u origin main  
#       GOTO GITHUB YOU SHOULD SEE YOUR CODE IN REPOSITORY NOW 
#       now you make changes to your code and want to push them to repository
# > git add .
# > git commit -m "change explanation"
# > git push origin main 
#       PUSHES CODE INTO GITHUB 
#       (if aws is linked code changes will be auto deployed onto webserver, via CodePipeline)

#       db support requirements
# > pip install Flask-SQLAlchemy

#       sending JSON with PUT/POST
#       if using request object 
#> requests.put(url, json=data2)
        if using curl
#> curl http://localhost:5000/video json={dictionary} 

# 1/24/2023 AWS error and fix, 
# 1/24/2023 fix for : Error: pg_config executable not found. (needed for psycopg2)
# 1/24/2023 contd. one option is to install the binaries vs having all files avail for build
# 1/24/2023 contd. psycopg2-binary==2.9.5   (place in requirements.txt, this will install binaries)
# 1/24/2023 contd. otherwise, you will need to use platform hooks to pre-install the dependencies that are needed to compile it 

# 1/24/23 AWS application files location
# 1/24/23 location of my application files which eleastic beanstalk has deployed on my behalf:
# 1/24/23 /var/app/current
# 1/24/23 in the /tmp/deployment/application folder during deployment and the moved to /var/app/current afterward

# 1/24/23 AWS log files location
# 1/24/23 location of log files while EB is deploying my application via codepipeline:
# 1/24/23 /var/log
# 1/24/23 /var/log/eb-engine.log has been beneficial to see errors while EB is installing my app, 
# 1/24/23 lib dependency issues have been found here

# CORS  documentation: https://flask-cors.corydolphin.com/en/latest/api.html#extension
# For now I am using the following line of code in specific endpoint functions:
#     temp_token.headers.add("Access-Control-Allow-Origin", "*")
# If you require the client to pass authentication headers (e.g. cookies) 
# the value can not be * — it must be a fully qualified domain!    

# Flask-CORS supports blueprints out of the box. Simply pass a blueprint instance 
# to the CORS extension, and everything will just work.
# One of the simplest configurations. Exposes all resources matching /api/* to
# CORS and allows the Content-Type header, which is necessary to POST JSON
# cross origin.
# CORS(app, resources=r'/api/*')

# Flask-CORS by default doesn't allow cookies.  To allow cookies or authenticated 
 # requests to be made cross origins, set "supports_credentials" option to True
 # app = Flask(__name__)
 # CORS(app, supports_credentials=True)

