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

