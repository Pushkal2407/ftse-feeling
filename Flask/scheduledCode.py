import schedule
import time
import requests
from datetime import datetime,timedelta
import psycopg2
from flask import Flask
from flask_mail import Mail ,Message
from DB_funcs import updateStockInfo, populateFundementals,get_companies_data
DB_URL='postgresql://James:y0jJqW14yMBSvQrUcJ_XhQ@test-cluster-5353.6zw.aws-eu-west-1.cockroachlabs.cloud:26257/APP_DB?sslmode=verify-full' # the database connection URL




# initial configuration of the this second app to run repeated tasks
app = Flask(__name__)
app.secret_key = "Zb4gqw3twSIDvqNXadtD"
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

app.config['MAIL_SUPPRESS_SEND'] = True # True - dont send mail, False - do send mail





# The function that is to be run repeatedly every 15 minutes 
# for getting extreme events and sending notifications accordingly
def repeatedTask():
    updateStockInfo() # update the store stock values (for etxreme stock changes)
    populateFundementals() # update the fundemental data of companies 
    newsDict = get_extreme_news_companies() # get the dict of companies with extreme news
    stockDict = get_extreme_stock_changes()# get the dict of companies with extreme stock changes
    # merge these entires to get a single list of tickers to notify users who follow them
    tickerList = newsDict["high sentiment"] + newsDict["low sentiment"] + stockDict["high sentiment"] +stockDict["low sentiment"]
    send_mail_notifications(get_mailing_list(tickerList)) # get the mailing list of users who follow these companies and send them mail notifications



# set the current time minus 15 once initially, this is then updated afterwards in the loop
now = datetime.now()- timedelta(hours=0, minutes=15)
last_fetch_time = now.strftime("%Y%m%dT%H%M")

# a function for getting the companies with news with  high or low sentiment
# Returns: a dictionary with keys "high sentiment" and "low sentiment". in each key is an array of tickers and their corresponding stories
def get_extreme_news_companies():
    global last_fetch_time # access the last fetch time

    high_sentiment=[] # initialise the arrays
    low_sentiment=[]

    for company_data in get_companies_data(): # for each company on the database
        ticker = company_data[0] # get theri ticker
        # query alpha vanatge to get news that has occured in the last 15 mins (since last fetch time)
        url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&time_from={last_fetch_time}&sort=RELEVANCE&LIMIT=50&apikey=UGACXLHBY5FDJCEW'
        r = requests.get(url)
        try:
            stories = (r.json())["feed"] # get the stories

            high_relevant_stories=[] # initialise the arrays
            low_relevant_stories=[]

            for story in stories: # for each story about the company
                sentiment = story["overall_sentiment_score"]
                if sentiment >=0.35: # good company news
                    high_relevant_stories.append(story) # add to the array of good news

                elif sentiment <=-0.35: # bad company news
                    low_relevant_stories.append(story) # add to the array of bad news

            if len(high_relevant_stories)!=0: # if the lists aren't empty then there is noteworthy news about the company and so add them to the list
                high_sentiment.append((ticker,high_relevant_stories))
            if len(low_relevant_stories)!=0:
                low_sentiment.append((ticker,low_relevant_stories))

        except:
            continue # if we error, move on to the next ticker
    last_fetch_time = update_time() # finally update the last time the news was fetched
    return {"high sentiment":high_sentiment, "low sentiment":low_sentiment} # return the dictionary


# a function to update the last fetch time to the current time
def update_time():
    global last_fetch_time
    now = datetime.now()
    last_fetch_time = now.strftime("%Y%m%dT%H%M") # set the last fetch time to now in the format needed


# a function for getting the companies with stocks with large increases and decreases
# Returns: a dictionary with keys "high sentiment" and "low sentiment". in each key is an array of tickers and their corresponding stories
def get_extreme_stock_changes():
    positive_extreme_stock_info=[]
    negative_extreme_stock_info=[]

    # sql statement to get all tickers and their closing value from yesterday
    sql = """
            SELECT ticker,closevalue
            FROM Stock;
        """
    current_values = []
    try:
        conn = psycopg2.connect(DB_URL) ## connect to the DB
        with  conn.cursor() as cur:
            # run the select statement 
            cur.execute(sql)

            current_values = cur.fetchall() # get all results in an array

            conn.close() # close the db connection
    except (Exception, psycopg2.DatabaseError) as error: # catch any errors
        print(error)    
    finally:

        start_values=[] # store the values

        for i in range(len(current_values)): # for companies
            start=start_values[i]
            ticker,close= current_values[i] # get and then compare the closing and starting values
            if (close-start)/start >0.10: # if a 10% increase in price in the day
                positive_extreme_stock_info.append((ticker,start,close)) # add to the array of large increases
            if (close-start)/start <-0.10: # if a 10% decrease in price in the day
                negative_extreme_stock_info.append((ticker,start,close))# add to the array of large decreases
    return {"positive":positive_extreme_stock_info, "negative":negative_extreme_stock_info} # return the dictionary



#a function to get the list of all people to mail for notifications
# Inputs : data - an array of form [(ticker,[stories]),...)
# Returns :mailing_list -  a dictionary wth keys of each ticker. the corresponding value will be an array of emails
def get_mailing_list(data):
    mailing_list={} # initiliase the mailing list

    for news_data in data:
        ticker = news_data[0] # for each ticker that had an extreme event
        # get the emails of all users that follow that ticker
        sql = """
                SELECT email
                FROM Users
                JOIN Follow ON Users.userID = Follow.userID
                WHERE Follow.ticker = %s ;
            """
        emails = None
        try:
            conn = psycopg2.connect(DB_URL) ## connect to the DB
            with  conn.cursor() as cur:
                # run the select statement
                cur.execute(sql,(ticker,))

                emails = cur.fetchall() # get the results in an array

                mailing_list[ticker] = emails # add these emails to the dictionary

                conn.close() # close the db connection
        except (Exception, psycopg2.DatabaseError) as error: # catch any errors
            print(error)    
    
    return mailing_list #return the dictonary of users to email (keyed by ticker)



# a function to send email notifications to all emails specified on the mailing dictionary
# Inputs : mailing_dict - a dictionary, with tickers as keys and an array of the emails of users who follow that company as the value
def send_mail_notifications(mailing_dict):
        for ticker in mailing_dict: # for each ticker with an extreme event
            recipients = mailing_dict[ticker] # for each email following the company
            message = Message(subject="Notifcation about" + ticker,body="There has been some intersting news about " +ticker,recipients=recipients) #draft the email
            mail.send(message) # sent the email







# Schedule the task to run every 15 minutes
schedule.every(15).minutes.do(repeatedTask)

# Run the scheduled tasks indefinitely
while True:
   schedule.run_pending()
   time.sleep(1)



