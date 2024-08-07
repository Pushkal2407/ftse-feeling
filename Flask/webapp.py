
from flask import request, session,Flask, render_template, redirect, jsonify
from flask_mail import Mail ,Message
from flask_cors import CORS, cross_origin

from DB_funcs import *
from RecAlgo import *

import random
import json
from alpha_vantage.timeseries import TimeSeries
from model import make_prediction
from datetime import timedelta



# Variables for demo, set to None for normal usage 
demo_UID=None
demo_userdata=[]
demo_code=None
demo_reset_code=None
demo_email=None

# create the Flask app
app = Flask(__name__)
app.secret_key = "Zb4gqw3twSIDvqNXadtD"


CORS(app, supports_credentials=True)


## mail  setup stuff ##

# gmail email system 
app.config.update(dict(
    DEBUG = False,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'ftsefeeling@gmail.com',
    MAIL_PASSWORD = 'isvz jepr pobz vmbr',
    MAIL_DEFAULT_SENDER = 'ftsefeeling@gmail.com',
))
mail = Mail(app)

app.config['MAIL_SUPPRESS_SEND'] = True # True - dont send, False - send mail


# Add CORS headers to every response
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'  # Set the allowed origin
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


## method for checking the login of a user
@app.route('/login', methods=["GET","POST"])
@cross_origin()
def login():
    global demo_UID
    if demo_UID != None: ## if the user is already logged in 
        return "already logged in" 

    if request.method =='POST': ## otherwise get their username  
        data = request.json
        email=data["email"]
        inputPassword=data["password"]

        ##check that all fields have been filled in
        for field in data:
            if data[field]=="":
                ## include fill in all fields message?
                return "Please fill in all form fields!"

    
        ## run the SQL command to check the User's details (function in db functions file)
        UID = check_user_details(email,inputPassword) # remember it returns None if the details dont match
        if UID == None: ## if there already is an account with this email then redirect them back to the registration page
            return "Wrong email or password"

        demo_UID = UID
        return "success" 
    return "can't GET" 
            



## method for checking the details of a user trying to register
@app.route('/register', methods=["POST"])
@cross_origin()
def register():
    global demo_UID, demo_userdata

    if demo_UID != None: ## if the user is already logged in 
        #and tries to go back to the login screen the should be taken to their home page
        return "already logged in" 

    if request.method =='POST':
        # get form data (sanitised in add_user function)

        data=request.json
        name=data["name"]
        email=data["email"]
        confirmEmail=data["confirmEmail"]
        inputPassword=data["password"]
        confirmPassword=data["confirmPassword"]

        ##check that all fields have been filled in
        for field in data:
            if data[field]=="":
                ## include fill in all fields message?
                return "Please fill in all form fields!"

        if email!=confirmEmail:# check emails entered match otherwise redirect them back to the registration page
            return "Emails don't match!"
        if inputPassword!=confirmPassword:# check re entered passwords match otherwise redirect them back to the registration page
            return "Passwords don't match!"
            
        # ## run the SQL command to add the user if there isnt an email already registered (function in db functions file)

        if get_user_details(email) != None: ## if there already is an account with this email then redirect them back to the registration page
            return "There's already an account with this email!"
        
        demo_userdata = [name,email,inputPassword]
        return "success"

    ## if it is not a POST request reload the page
    return "error"



## method for sending a verification email
@app.route('/sendVerification', methods=["GET"])
@cross_origin()
def sendVerification():
    global demo_userdata,demo_code

    if request.method=="GET":
        ## generate random 6 digit code
        code = ""
        for _ in range(6):
            code +=str(random.randint(0,9))
        demo_code = code
        recipients = [demo_userdata[1]]
        message = Message(subject="FTSE Feeling registration Email Verification",body="Here is the six digit verification code you just asked for " +code,recipients=recipients)
        mail.send(message)
        return "success" # go to the page to allow the user to enter the code



## method for checking verification codes and adding user
@app.route('/checkRegistrationCode', methods=["POST"])
@cross_origin()
def checkRegistrationCode():
    global demo_code,demo_userdata,demo_UID
    if request.method=="POST":
        if int(request.json["code"]) !=int(demo_code): ## if the user entered the wrong code
            return "wrong Code" # give them a notice about wrong code and allow them to try again 
        
        demo_code = None
        ## otherwise the user entered the right code so add them to the database

        data = demo_userdata # get their details
        demo_userdata = []

        ## run the SQL command to add the user if there isnt an email already registered (function in db functions file)
        UID = add_user(data[0],data[1],data[2]) # remember it returns None if there isn already an account registered otherwise its the user id
        if UID ==None:
            return "error"
        return "success"#return to the index page but logged in as a new user


# Method for logging out user 
@app.route('/logout', methods=["GET", "POST"])
@cross_origin()
def logout():
    global demo_UID
    demo_UID = None
    return "success"

# Determines if a user is logged in 
@app.route('/isLoggedIn')
def isLoggedIn():
    global demo_UID
    return "true"  if demo_UID!=None else "false"

# Gets the list of companies a user follows
@app.route("/getFollowed")
@cross_origin()
def getFollowed():
    global demo_UID

    return json.dumps({"data":get_followed(demo_UID)})

# Adds the entry to show a user is following a new company
@app.route("/addFollow", methods=["POST"])
@cross_origin()
def addFollow():
    global demo_UID
    if request.method=="POST":
        try:
            ticker = request.json["ticker"]
            add_follow(demo_UID,ticker)
            return "success"
        except:
            return "error"
    return "POST don't GET"

# Removes the entry representing the user following a company
@app.route("/removeFollow", methods=["POST"])
@cross_origin()
def removeFollow():
    global demo_UID
    if request.method=="POST":
        try:
            ticker = request.json["ticker"]
            remove_follow(demo_UID,ticker)
            return "success"
        except:
            return "error"
    return "POST don't GET" 
    
# Gets the list of recommended companies for a user
@app.route("/getRecommended")
@cross_origin()
def getRecommended():
    global demo_UID

    tickers = list(get_user_recommended_companies(demo_UID))
    return_list=[]
    for ticker in tickers:
        try:
            data = get_company_data(ticker)
            name = data[0]
            return_list.append([name,ticker])
        except:
            print("error")
    
    return json.dumps({"data":return_list})

# Gets the data for all the companies 
@app.route("/getCompaniesData")
@cross_origin()
def getCompaniesData():
    results = get_companies_data()
    logoLocation = "http://127.0.0.1:5000/static/companyLogos/"
    data=[]
    for i in range(len(results)):
        temp = list(results[i])
        temp.append(logoLocation+results[i][0]+".png")
        data.append(temp)
    return json.dumps({"data": data})



# Gets the fundamental data for a company (e.g. ebitda, ...)
@app.route("/getFundementals")
@cross_origin()
def getFundementals():
    ticker = request.args.get('ticker') 
    fundemental_data = list(get_company_fundementals(ticker))
    fundemental_data[1] = fundemental_data[1].strftime("%d/%m/%Y") ## casting datetime to a string so it can be sent using JSON
    return json.dumps({"data":fundemental_data})

# Gets the data for a specific company 
@app.route("/getCompanyData")
@cross_origin()
def getCompanyData():
    logoLocation = "http://127.0.0.1:5000/static/companyLogos/"
    ticker = request.args.get('ticker') 
    return_list = list(get_company_data(ticker))
    return_list.append(logoLocation+return_list[3]+".png")
    return json.dumps({"data":return_list})



# Sends the email needed to reset password
@app.route('/resetPasswordMail', methods=["POST"])
@cross_origin()
def resetPasswordMail():
    global demo_reset_code,demo_email

    if request.method=="POST":
        ## generate random 6 digit code
        code = ""
        for _ in range(6):
            code +=str(random.randint(0,9))
        demo_reset_code = code # store this code so we can check it later
        demo_email = request.json["email"]
        recipients = [demo_email]
        message = Message(subject="FTSE Feeling registration Password Reset", body="Please enter this code on the page shown: " + code,recipients=recipients)
        mail.send(message)

        return "success"  # go to the page to allow the user to enter the code



## Method for checking verification codes and adding user
@app.route('/checkPasswordCode', methods=["POST"])
@cross_origin()
def checkPasswordCode():
    global demo_reset_code,demo_email
    if request.method=="POST":
        if int(request.json["code"]) !=int(demo_reset_code): # if the user entered the wrong code
            return "codes don't match" # give them a notice about wrong code and allow them to try again
        
        update_password(demo_email,request.json["password"])
        demo_reset_code=None
        demo_email = None

        return "password updated"
    


#Method for changing password when the user is logged in (from the profile page) dont need a code/authentication
@app.route('/changePassword', methods=["POST"])
@cross_origin()
def changePassword():
    global demo_UID
    if request.method=="POST":
        email = getEmailFromUID(demo_UID)
        update_password(email,request.json["password"])
        return "success"
    

# Gets the email address of user 
@app.route('/fetchEmail', methods=["POST", "GET"])
@cross_origin()
def fetchEmail():
    global demo_UID
    if request.method=="GET":
        email = getEmailFromUID(demo_UID)
        return jsonify({"email": email})  
    
# Gets the interests of user
@app.route('/fetchInterest', methods=["POST", "GET"])
@cross_origin()
def fetchInterest():
    global demo_UID
    if request.method=="GET":
        interest = getInterestFromUID(demo_UID)
        return jsonify({"interest": interest})  # Return the email as JSON
    
# Gets the name of user
@app.route('/fetchName', methods=["POST", "GET"])
@cross_origin()
def fetchName():
    global demo_UID
    if request.method=="GET":
        name = getNameFromUID(demo_UID)
        return jsonify({"name": name})  # Return the email as JSON
    


# Gets the stock graph for given company/ticker
@app.route('/getGraphData', methods=["GET"])
@cross_origin()
def getGraphData():
    ticker = request.args.get('ticker') 
    ts2 = TimeSeries(key="UGACXLHBY5FDJCEW", output_format='csv') # get the data for the graph as a csv reader
    data = (ts2.get_daily_adjusted(symbol=ticker, outputsize='full'))[0] 
    dates=[]
    values=[]
    for row in data: # get the dates and their corresponding closing values (as needed for the graph input)
        dates.append(row[0])
        values.append(row[4])
    dates.reverse()
    values.reverse()
        

    return json.dumps({"xValues":dates[1:],"yValues":values[1:]}) #skim the first item in each array and return it

# Gets the forecast stock price for given company/ticker 
@app.route("/getPrediction")
@cross_origin()
def getPrediction():
    ticker = request.args.get('ticker')
    prediction = str(make_prediction(ticker)) # get the prediction and pass it through
    return json.dumps({"data":prediction})
