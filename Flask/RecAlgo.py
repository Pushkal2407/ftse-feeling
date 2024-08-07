import numpy as np  
from sklearn.metrics.pairwise import cosine_similarity  
import psycopg2  


DB_URL='postgresql://James:y0jJqW14yMBSvQrUcJ_XhQ@test-cluster-5353.6zw.aws-eu-west-1.cockroachlabs.cloud:26257/APP_DB?sslmode=verify-full'


# Establishes a connection to the PostgreSQL database 
def get_db_connection():
    return psycopg2.connect(DB_URL)


# Retrieves each user's followed companies from the database
def fetch_users_data():
    users_data = {}  
    with get_db_connection() as conn:  # Uses the connection function to connect to the database
        with conn.cursor() as cur: 
            # Executes an SQL query to select users and their followed companies
            cur.execute("""
                SELECT Users.userID, Users.interests, array_agg(Follow.ticker) as followed_companies
                FROM Users
                JOIN Follow ON Users.userID = Follow.userID
                GROUP BY Users.userID;
            """)
            users_data = cur.fetchall()
    conn.close()
    return users_data

# Creates a mapping of company tickers to a unique index 
def fetch_company_index():
    company_index = {}  
    with get_db_connection() as conn:  # Database connection
        with conn.cursor() as cur:  
            cur.execute("SELECT ticker FROM Company")  # Selects all company tickers
            for idx, row in enumerate(cur.fetchall()):
                company_index[row[0]] = idx
    conn.close()
    return company_index

# Encodes a list of companies into a binary vector based on the company index
def encode_companies(companies, company_index):
    vector = np.zeros(len(company_index))  # Initializes a zero vector of the size of the company index
    for company in companies:  
        if company in company_index:  
            vector[company_index[company]] = 1  # Sets the corresponding vector element to 1
    return vector

# Recommends companies to a user based on the preferences of similar users
def recommend_companies(user_id, users_data, company_index,current_user_data, similarity_threshold=0.5):
    current_user_companies = current_user_data[2]  # Followed companies
    current_user_interests = current_user_data[1]  # Interests 
    
    # Encodes the current user's followed companies into a vector
    current_user_vector = encode_companies(current_user_companies, company_index)
    
    similar_users = []  # List to store similar users
    # Iterates over other users to find similarities
    for other_user_data in users_data:
        other_user_id, other_user_interests, other_user_following = other_user_data
        interests_match = True
        if other_user_interests != None and other_user_interests != None:
            interest_intersection = [value for value in current_user_interests if value in other_user_interests]
            if len(interest_intersection) ==0:
                interests_match = False

        if other_user_id != user_id and interests_match: 
            other_user_vector = encode_companies(other_user_following, company_index)
            similarity = cosine_similarity([current_user_vector], [other_user_vector])[0][0]

            # Adds the user to the similar users list if the similarity is above the threshold
            if similarity >= similarity_threshold:
                similar_users.append(other_user_data)
    
    recommended_companies = set()  
    # Adds the followed companies of similar users to the recommendations
    for user in similar_users:
        recommended_companies.update(user[2])
    
    # Removes companies the current user already follows from the recommendations
    recommended_companies.difference_update(current_user_companies)
    
    return recommended_companies

# Retrieves each user's followed companies from the database
def get_user_data(UID):
    users_data = {}  
    with get_db_connection() as conn: 
        with conn.cursor() as cur:  
            # Executes an SQL query to select users and their followed companies
            cur.execute("""
                SELECT Users.userID, Users.interests, array_agg(Follow.ticker) as followed_companies, array_agg(Company.companyName) as company_names
                FROM Users
                LEFT JOIN Follow ON Users.userID = Follow.userID
                LEFT JOIN Company ON Company.ticker = Follow.ticker
    
                WHERE Users.userID = %s
                GROUP BY Users.userID;
            """,(UID,))
            users_data = cur.fetchone()
    conn.close()
    print(users_data)
    return users_data

# Retrieves each user's recommended companies 
def get_user_recommended_companies(UID):
    users_data = fetch_users_data()  # Fetches all users' data
    company_index = fetch_company_index()  # Fetches the company index
    user_data = get_user_data(UID)
    recommendations = recommend_companies(user_data[0], users_data, company_index, user_data)
    return recommendations




