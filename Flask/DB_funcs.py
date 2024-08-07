import psycopg2
from werkzeug import security
from markupsafe import escape
import yfinance as yf
import requests


# the database connection URL
DB_URL='postgresql://James:y0jJqW14yMBSvQrUcJ_XhQ@test-cluster-5353.6zw.aws-eu-west-1.cockroachlabs.cloud:26257/APP_DB?sslmode=verify-full'

# a fixed array of all FTSE 100 companies and their tickers - only used in intial population of the stock table
companyData=[["3i","III"],
["Admiral Group","ADM"],
["Airtel Africa","AAF"],
["Anglo American plc","AAL"],
["Antofagasta plc","ANTO"],
["Ashtead Group","AHT"],
["Associated British Foods","ABF"],
["AstraZeneca","AZN"],
["Auto Trader Group","AUTO"],
["Aviva","AV"],
["B&M","BME"],
["BAE Systems","BA"],
["Barclays","BARC"],
["Barratt Developments","BDEV"],
["Beazley Group","BEZ"],
["Berkeley Group Holdings","BKG"],
["BP","BP"],
["British American ","BATS"],
["BT Group","BT-A"],
["Bunzl","BNZL"],
["Burberry","BRBY"],
["Centrica","CNA"],
["Coca-Cola HBC","CCH"],
["Compass Group","CPG"],
["Convatec","CTEC"],
["Croda International","CRDA"],
["DCC plc","DCC"],
["Diageo","DGE"],
["Diploma","DPLM"],
["Endeavour Mining","EDV"],
["Entain","ENT"],
["Experian","EXPN"],
["Foreign & Colonial Investment Trust","FCIT"],
["Flutter Entertainment","FLTR"],
["Frasers Group","FRAS"],
["Fresnillo plc","FRES"],
["Glencore","GLEN"],
["GSK plc","GSK"],
["Haleon","HLN"],
["Halma plc","HLMA"],
["Hikma Pharmaceuticals","HIK"],
["Howdens Joinery","HWDN"],
["HSBC","HSBA"],
["IHG Hotels & Resorts","IHG"],
["IMI","IMI"],
["Imperial Brands","IMB"],
["Informa","INF"],
["Interte Capital Group","ICP"],
["International Airlines Group","IAG"],
["Intertek","ITRK"],
["JD Sports","JD"],
["Kingfisher plc","KGF"],
["Land Securities","LAND"],
["Legal & General","LGEN"],
["Lloyds Banking Group","LLOY"],
["London Stock Exchange Group","LSEG"],
["M&G","MNG"],
["Marks & Spencer","MKS"],
["Melrose Industries","MRO"],
["Mondi","MNDI"],
["National Grid plc","NG"],
["NatWest Group","NWG"],
["Next plc","NXT"],
["Ocado Group","OCDO"],
["Pearson plc","PSON"],
["Pershing Square Holdings","PSH"],
["Persimmon","PSN"],
["Phoenix Group","PHNX"],
["Prudential plc","PRU"],
["Reckitt","RKT"],
["RELX","REL"],
["Rentokil Initial","RTO"],
["Rightmove","RMV"],
["Rio Tinto","RIO"],
["Rolls-Royce Holdings","RR"],
["RS Group plc","RS1"],
["Sage Group","SGE"],
["Sainsbury's","SBRY"],
["Schroders","SDR"],
["Scottish Mortgage Investment Trust","SMT"],
["Segro","SGRO"],
["Severn Trent","SVT"],
["Shell plc","SHEL"],
["DS Smith","SMDS"], 
["Smiths Group","SMIN"], 
["Smith & Nephew","SN"],
["Smurfit Kappa","SKG"],
["Spirax-Sarco Engineering","SPX"],
["SSE plc","SSE"],
["Standard Chartered","STAN"],
["St. James's Place plc","STJ"],
["Taylor Wimpey","TW"],
["Tesco","TSCO"],
["Unilever","ULVR"],
["United Utilities","UU"],
["Unite Group","UTG"],
["Vodafone Group","VOD"],
["Weir Group","WEIR"],
["Whitbread","WTB"],
["WPP plc","WPP"]]






# a function to delete a user from the database using their email
# Inputs : email - the email fo the user to delete
def delete_user(email):
    # delete the user from the DB
    sql = """
            DELETE FROM Users
            WHERE email=%s;
            """
    try:
        conn = psycopg2.connect(DB_URL) ## connect to the DB

        with  conn.cursor() as cur:
            # execute the statement
            cur.execute(sql, (email,))
  
            conn.commit() # commit the changes to the database
            conn.close() # close the db connection
    except (Exception, psycopg2.DatabaseError) as error: # catch any errors
        print(error) 




# a function to check if an account with the same email exists and
# if it doesn't then use the inputted user details and try to add them to the table
# Returns the user ID (int) if successfully added, None otherwise
def add_user(name:str,email:str,password:str,interests=None) -> int: 

    # sanitise inputs
    input_name = escape(name)
    input_email = escape(email)
    input_password = escape(password)

    ##Insert a new user into the users table if there is no account with the same email already registered
    sql = """
            INSERT INTO Users(fullname,email,phash,interests)
            VALUES(%s,%s,%s,%s)
            ON CONFLICT (email) DO NOTHING
            RETURNING userID;
        """
    user_id = None
    try:
        conn = psycopg2.connect(DB_URL) ## connect to the DB

        with  conn.cursor() as cur:
            # execute the INSERT statement
            cur.execute(sql, (input_name,input_email,security.generate_password_hash(input_password),interests))

            # get the generated id back                
            rows = cur.fetchone()
            if rows: # if the query executed correctly get the user id
                user_id = rows[0]

            
            conn.commit() # commit the changes to the database
            conn.close() # close the db connection
    except (Exception, psycopg2.DatabaseError) as error: # catch any errors
        print(error)    
    finally:
        return user_id #  return the user id which will be an int if the insert worked, and None if it didnt



# a function to check a user's login details and see if they match the Db's stored values
# Returns the user ID (int) if the user's details, None otherwise
def check_user_details(email:str,password:str) ->int: 

    # sanitise inputs
    input_email = escape(email)
    input_password = escape(password)

    ##Insert a new user into the users table if there is no account with the same email already registered
    sql = """
            SELECT userID, phash
            FROM Users
            WHERE email = %s ;
        """
    user_id = None
    try:
        conn = psycopg2.connect(DB_URL) ## connect to the DB
        with  conn.cursor() as cur:
            # run the select statement
            cur.execute(sql,(input_email,))

            # get the id and password hash      
            userdata = cur.fetchone()

            if userdata == None: ## checking we have results
                UID = None
                phash = None
            else:
                UID = userdata[0]
                phash = userdata[1]

            if phash: # if there is a user with that email address
                ## check hash
                if security.check_password_hash(escape(phash),input_password): ## if the password hashes match then the user has the right details
                    user_id = UID # this step is done to ensure that user_id isn't returned if the emails match but the passwords dont

            conn.close() # close the db connection
    except (Exception, psycopg2.DatabaseError) as error: # catch any errors
        print(error)    
    finally:
        return user_id #  return the user id which will be an int if the insert worked, and None if it didnt





# a function to get a user's details 
# Returns the an array of the user's details if the user exists, None otherwise
def get_user_details(email:str) ->list[str]: 

    # sanitise inputs
    input_email = escape(email)

    ##Insert a new user into the users table if there is no account with the same email already registered
    sql = """
            SELECT *
            FROM Users
            WHERE email = %s ;
        """
    userdata = None
    try:
        conn = psycopg2.connect(DB_URL) ## connect to the DB
        with  conn.cursor() as cur:
            # run the select statement
            cur.execute(sql,(input_email,))

            # get the id and password hash      
            userdata = cur.fetchone()

            conn.close() # close the db connection
    except (Exception, psycopg2.DatabaseError) as error: # catch any errors
        print(error)    
    finally:
        return userdata #  return the user id which will be an int if the insert worked, and None if it didnt









# a function to get a all the companies' board members and their titles. this is used to populate the DB
# Returns the an array of the FTSE 100 companies' board members and their titles as provided by yfinance
# (if the company isn't covered by AV then the company's board will be null)
def getBoardMembers()->list[str]:

    boardDetails=[]
    for ticker in [item[1] for item in companyData]: # for each ticker in the companyData array
        exec=[]
        ticker+=".L" # adaptation for yfinance as this gives more accurate results
        
        pc = yf.Ticker(ticker)
        try:
            for item in (pc.info['companyOfficers']):
                exec.append([item["name"], item["title"]]) # get a list fo the company executives and their titles
        except:
            exec.append(None) # if the data isn't there then set it to null
        finally:
            boardDetails.append(exec) # add the data to a master array for all companies
    return boardDetails


# a function to get a all the companies descriptions. this is used to populate the DB
# Returns the an array of the FTSE 100 companies descriptions as provided by alpha vantage
# (if the company isn't covered by AV then the company's description will be null)
def getDescriptions() ->list[str]:
    descriptions = []
    for ticker in [item[1] for item in companyData]:# for each ticker in the companyData array
        try:
            url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey=UGACXLHBY5FDJCEW'
            r = requests.get(url)
            data = r.json() #query alpha vantage for the company descriptions 
            r.close()
            descriptions.append(data["Description"]) # add these descriptions to an array
        except:
            descriptions.append(None) # if the description doesn't exists set it to null
    return descriptions # return the array of descriptions


# a function to get a all the companies sectors. this is used to populate the DB
# Returns the an array of the FTSE 100 companies' sectors as provided by alpha vantage
# (if the company isn't covered by AV then the company's sector will be null)
def getSectors() ->list[str]:
    sectors = []
    for ticker in [item[1] for item in companyData]:
        try:
            url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey=UGACXLHBY5FDJCEW'
            r = requests.get(url)
            data = r.json() #query alpha vantage for the company sectors 
            r.close()
            sectors.append(data["Sector"])# add these sectors to an array
        except:
            sectors.append(None)# if the sector isn't stored then set it to null
    return sectors# return the array of sectors



# the overall function to populate the company table. This should only be done once at the beginning, or if the table has been dropped
def populate_company_table():

    executives=getBoardMembers() # get the board members, descriptions and sectors of each company
    descriptions = getDescriptions()
    sectors = getSectors()

    try:
        conn = psycopg2.connect(DB_URL) ## connect to the DB
        
        sql = """
            INSERT INTO Company (companyname,ticker,executives,description,sector) VALUES
            (%s,%s,%s,%s,%s)
            ON CONFLICT DO NOTHING;
            """
        with conn.cursor() as cur:
            for i in range(100) :

                cur.execute(sql,(companyData[i][0],companyData[i][1],executives[i],descriptions[i],sectors[i])) # insert the corresponding values into the company database

                
        conn.commit() # commit the changes to the database
        conn.close() # close the db connection
    except (Exception, psycopg2.DatabaseError) as error: # catch any errors
        print(error)

        



# a function to update the info stored in the stock table. To be run every 15 mins by the scheduled code
def updateStockInfo():
    for company in companyData: # for each company ticker
        ticker = company[1]            
        try:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=15min&outputsize=compact&symbol={ticker}&apikey=UGACXLHBY5FDJCEW'
            r = requests.get(url)
            data = r.json() # query alpha vantage for the stock data
            r.close()
            latestTime = data["Meta Data"]["3. Last Refreshed"] # get the latest refresh time and the stock data for it
            latestInfo = data["Time Series (15min)"][latestTime]

        
            conn = psycopg2.connect(DB_URL) ## connect to the DB
            sql = """
                INSERT INTO Stock (ticker,updateTime,openValue,highValue,lowValue,closeValue,volume) VALUES
                (%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (ticker) DO UPDATE SET (updateTime, openValue, highValue, lowValue, closeValue, volume) = (excluded.updateTime, excluded.openValue, excluded.highValue, excluded.lowValue, excluded.closeValue, excluded.volume);
                """
            with conn.cursor() as cur:
                cur.execute(sql,(ticker,latestTime,latestInfo["1. open"],latestInfo["2. high"],latestInfo["3. low"],latestInfo["4. close"],latestInfo["5. volume"])) # add the data to the database

                    
            conn.commit() # commit the changes to the database
            conn.close() # close the db connection
        
        except (Exception, psycopg2.DatabaseError) as error: # catch any errors
            print(error)



            






# a function to populate the fundementals table. To be run sporadically to esnrue company data is kept up to date
def populateFundementals():
    for company in companyData:
        ticker = company[1]
        try:
            url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey=UGACXLHBY5FDJCEW'
            r = requests.get(url)
            data = r.json() # query alpha vantage for the fundementals data
            r.close()

            # get the corresponding items of data
            EBITDA = data["EBITDA"]
            reportDate = data["LatestQuarter"]
            revenue = data["RevenueTTM"]
            netProfit = data["GrossProfitTTM"]

            conn = psycopg2.connect(DB_URL) ## connect to the DB
            sql = """

            INSERT INTO Fundementals (ticker, reportDate, revenueTTM, netGrossProfit, ebitda)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (ticker) DO UPDATE
            SET (reportDate, revenueTTM, netGrossProfit, ebitda) = (excluded.reportDate, excluded.revenueTTM, excluded.netGrossProfit, excluded.ebitda);

            """
            with conn.cursor() as cur:
                cur.execute(sql,(ticker,reportDate,revenue,netProfit,EBITDA)) # execute the sql and add the to the database

                    
            conn.commit() # commit the changes to the database
            conn.close() # close the db connection
        except (Exception, psycopg2.DatabaseError) as error: # catch any errors
            print(error)
    




# a function to get a user's details 
# Inputs : an integer of the UID of the user
# Returns : An array of the user's details in the order specified in the schema if the user exists, None otherwise
def get_followed(UID) ->list[str]: 

    sql = """
        SELECT companyName,Company.ticker
        FROM Company
        INNER JOIN Follow ON Follow.ticker = Company.ticker
        WHERE Follow.userID = %s;
        """
    followed = None
    try:
        conn = psycopg2.connect(DB_URL) ## connect to the DB
        with  conn.cursor() as cur:
            # run the select statement

            cur.execute(sql,(UID,))
             
            followed = cur.fetchall()

            conn.close() # close the db connection
    except (Exception, psycopg2.DatabaseError) as error: # catch any errors
        print(error)    
    finally:
        return followed #  return the user id which will be an int if the insert worked, and None if it didnt




# a function to add an entry to the follow table for a user and a company
# Inputs: UID - an integer, the UID of the user who's following the company
#   - ticker - the ticker of the company to follow
def add_follow(UID,ticker):
        try:
            conn = psycopg2.connect(DB_URL) ## connect to the DB
            sql = """

            INSERT INTO Follow (userID, ticker)
            VALUES (%s, %s)
            ON CONFLICT (userID,ticker) DO NOTHING;

            """
            with conn.cursor() as cur:
                cur.execute(sql,(UID,ticker)) # add the UID, ticker pair to the table

                    
            conn.commit() # commit the changes to the database
            conn.close() # close the db connection
        except (Exception, psycopg2.DatabaseError) as error: # catch any errors
            print("error")
            print(error)






# a function to remove an entry to the follow table for a user and a company
# Inputs: UID - an integer, the UID of the user who's following the company
#   - ticker - the ticker of ticker to remove the follow
def remove_follow(UID,ticker):
        try:


            conn = psycopg2.connect(DB_URL) ## connect to the DB
            sql = """

            DELETE FROM Follow
            WHERE userID = %s AND ticker = %s 

            """
            with conn.cursor() as cur:
                cur.execute(sql,(UID,ticker)) # remove the UID, ticker pair from the table

                    
            conn.commit() # commit the changes to the database
            conn.close() # close the db connection
        except (Exception, psycopg2.DatabaseError) as error: # catch any errors
            print("error")
            print(error)



# a function to get the details of all companies stored on the database from the company table
# Returns : An array of the the companies data
def get_companies_data() ->list[str,str,str]: 

    sql = """
        SELECT ticker, companyName
        FROM Company;
        """
    compData = None
    try:
        conn = psycopg2.connect(DB_URL) ## connect to the DB
        with  conn.cursor() as cur:
            # run the select statement

            cur.execute(sql,) # run the query
             
            compData = cur.fetchall() # and get the result

            conn.close() # close the db connection
    except (Exception, psycopg2.DatabaseError) as error: # catch any errors
        print(error)    
    finally:
        return compData # return the data











# a function to get the details of the specified companies stored on the database from the fundementals table
# Inputs: ticker - the ticker to get the data for
# Returns : An array of the the companies data
def get_company_fundementals(ticker) ->list[str,str,str]: 

    sql = """
        SELECT *
        FROM Fundementals
        WHERE ticker = %s;
        """
    fundementals = None
    try:
        conn = psycopg2.connect(DB_URL) ## connect to the DB
        with conn.cursor() as cur:
            # run the select statement

            cur.execute(sql,(ticker,)) # run the query
             
            fundementals = cur.fetchone() # and get the result

            conn.close() # close the db connection
    except (Exception, psycopg2.DatabaseError) as error: # catch any errors
        print(error)    
    finally:
        return fundementals # return the results



# a function to get the details of the specified company's stored on the database from the company table
# Inputs: ticker - the ticker to get the data for
# Returns : An array of the the company's data
def get_company_data(ticker) ->list[str,str,str,str]: 

    sql = """
        SELECT *
        FROM Company
        WHERE ticker = %s;
        """
    data = None
    try:
        conn = psycopg2.connect(DB_URL) ## connect to the DB
        with  conn.cursor() as cur:
            # run the select statement

            cur.execute(sql,(ticker,))# run the query
             
            data = cur.fetchone()# and get the result

            conn.close() # close the db connection
    except (Exception, psycopg2.DatabaseError) as error: # catch any errors
        print(error)    
    finally:
        return data # return the results






# a function to update the password hash stored on the database for a user
# Inputs : email - the email of the user to chaneg the password has for
#   - pword - thepassword of the user to hash and then store
def update_password(email,pword):
    sql = """
                UPDATE Users
                SET phash = %s
                WHERE email=%s;
            """

    try:
        conn = psycopg2.connect(DB_URL) ## connect to the DB

        with  conn.cursor() as cur:
            cur.execute(sql, (security.generate_password_hash(pword),email,)) # run the sql with the paswword hashed
          

            conn.commit() # commit the changes to the database
            conn.close() # close the db connection
    except (Exception, psycopg2.DatabaseError) as error: # catch any errors
        print(error)




# a function to get the email of a user from their UID
# Inputs : uid - the integer user id of the user
# Returns : email - the email of the user
def getEmailFromUID(uid):
    input_uid = escape(uid)
    sql = """
            SELECT email
            FROM Users
            WHERE userID=%s;
        """
    useremail= None
    try:
        conn = psycopg2.connect(DB_URL) ## connect to the DB

        with  conn.cursor() as cur:
            cur.execute(sql, (input_uid,)) # run the query
            useremail = cur.fetchone() # get the results
          
            conn.close() # close the db connection
    except (Exception, psycopg2.DatabaseError) as error: # catch any errors
        print(error)
    finally:
        return useremail # return the results


# a function to get the interests of a user from their UID
# Inputs : uid - the integer user id of the user
# Returns : interests - an array of strings of the interests of the user
def getInterestFromUID(uid):
    input_uid = escape(uid)
    sql = """
            SELECT interests
            FROM Users
            WHERE userID=%s;
        """
    userinterest= None
    try:
        conn = psycopg2.connect(DB_URL) ## connect to the DB

        with  conn.cursor() as cur:
            cur.execute(sql, (input_uid,))# run the query
            userinterest = cur.fetchall()# get the results
          
            conn.close() # close the db connection
    except (Exception, psycopg2.DatabaseError) as error: # catch any errors
        print(error)
    finally:
        return userinterest
    


# a function to get the name of a user from their UID
# Inputs : uid - the integer user id of the user
# Returns : name - the name of the user
def getNameFromUID(uid):
    input_uid = escape(uid)
    sql = """
            SELECT fullname
            FROM Users
            WHERE userID=%s;
        """
    username= None
    try:
        conn = psycopg2.connect(DB_URL) ## connect to the DB

        with  conn.cursor() as cur:
            cur.execute(sql, (input_uid,))
            username = cur.fetchone()
          
            conn.close() # close the db connection
    except (Exception, psycopg2.DatabaseError) as error: # catch any errors
        print(error)
    finally:
        return username



# a function to populate the database with test data
def add_test_data(): # DROP the database before (or dont to test duplicate data entry)
    add_user("test1","test1@mail.com","test1")
    add_user("test2","test2@mail.com","test2")
    add_user("test3","test3@mail.com","test3")
    add_user("test4","test4@mail.com","test4")
    add_user("test5","test5@mail.com","test5")
    populate_company_table()

    uid1 = get_user_details("test1@mail.com")[0]
    uid2 = get_user_details("test2@mail.com")[0]
    uid3 = get_user_details("test3@mail.com")[0]
    uid4 = get_user_details("test4@mail.com")[0]
    uid5 = get_user_details("test5@mail.com")[0]

    # shares many follows but has less than others
    add_follow(uid1,"BP")
    add_follow(uid1,"RR")
    add_follow(uid1,"AAL")
    add_follow(uid1,"GSK")

    # some shared with 1 and 5
    add_follow(uid2,"BP")
    add_follow(uid2,"RR")
    add_follow(uid2,"BA")
    add_follow(uid2,"FRES")
    add_follow(uid2,"CPG")
    add_follow(uid2,"GSK")
    add_follow(uid2,"SHEL")

    # some shared with 1,2,3 and 5
    add_follow(uid3,"BP")
    add_follow(uid3,"TSCO")
    add_follow(uid3,"AAL")
    add_follow(uid3,"SN")
    add_follow(uid3,"RTO")
    add_follow(uid3,"NXT")


    # no shared companies
    add_follow(uid4,"JD")
    add_follow(uid4,"III")
    add_follow(uid4,"LAND")
    add_follow(uid4,"IAG")
    add_follow(uid4,"MRO")
    add_follow(uid4,"PRU")

    # a mix of user2 and 3s followed companies
    add_follow(uid5,"BP")
    add_follow(uid5,"RR")
    add_follow(uid5,"BA")
    add_follow(uid5,"SN")
    add_follow(uid5,"RTO")
    add_follow(uid5,"NXT")

    updateStockInfo()

    populateFundementals()
