
import pandas as pd 
import requests
from os import getenv
import datetime
from sys import stderr

# Fetches all historical OHCLV values for given ticker from AlphaVantage
def downloadStockData(ticker:str="HSBA.LON", outputsize:str="full") -> bool:

    # Check that valid value was passed for outputsize, valid values are 'compact' and 'full' 
    if outputsize not in ["compact", "full"]:
        print(f"ERROR: Invalid value '{outputsize}' for 'outputsize' parameter, can only take values 'compact' or 'full'.", file=stderr)
        return False

    # Access AlphaVantage API key (stored as environment variable)
    avKey = "UGACXLHBY5FDJCEW"#getenv('AV_KEY')
    # If AV_KEY not set, getenv will return None 
    if not avKey:
        print("ERROR: Please store Alpha Vantage API Key in environment variable 'AV_KEY' using '$Env:AV_KEY='{YOUR KEY}''", file=stderr)
        return False
    

    # Alpha Vantage endpoint for daily OHCLV stock data
    avEndpoint = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize={outputsize}&apikey={avKey}'

    try:
        # Send request for stock data from AlphaVantage
        avRequest = requests.get(avEndpoint)
        # Raises HTTPError for bad responses
        avRequest.raise_for_status()  
        # Access response data
        stockData = avRequest.json()


        # print(stockData)
        # Check that API didn't return an error message
        if "Error Message" in stockData:
            print("ERROR: Failed to fetch data. Please check API key and Ticker symbol.",  file=stderr)
            return False
        
        try:
            # Convert the returned stock data into a DataFrame with dates as rows and OHCLV as columns.
            stockDataframe = pd.DataFrame(stockData['Time Series (Daily)'])

            # Dataframe is initially oriented such that the rows and columns are flipped, so need to transpose the dataframe
            stockDataframe = stockDataframe.T # stockDataframe.transpose()

            # Also need to reverse order of rows so dates are in ascending order
            stockDataframe = stockDataframe.iloc[::-1]

            # Rename columns to be more descriptive 
            stockDataframe.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

            # Save to CSV
            stockDataframe.to_csv("HSBC_stockDataset.csv")
            
        # Thrown if 'Time Series (Daily)' data not found in response 
        except KeyError as k:
            print("ERROR: No stock data found in AlphaVantage response, please try again", file=stderr)
            return False 
        
        return True
    
    # Catch HTTPError thrown by raise_for_status() when handling API request
    except requests.RequestException as e:
        print(f"ERROR: HTTP request error: {e}", file=stderr)
        return False
        
    except Exception as e:
        # Handles all exceptions with a single message#
        print(f"ERROR: An error occurred: {e}", file=stderr)
        return False
    



def downloadNewsSentiment(ticker:str, time_from:str, limit:int=50) -> bool:

    # Access AlphaVantage API key (stored as environment variable)
    avKey = "UGACXLHBY5FDJCEW"#getenv('AV_KEY')
    # If AV_KEY not set, getenv will return None 
    if not avKey:
        print("ERROR: Please store Alpha Vantage API Key in environment variable 'AV_KEY'")
        return False
    
    # Alpha Vantage endpoint for news and sentiment
    avEndpoint = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&time_from={time_from}&limit={limit}&apikey={avKey}'

    try:
        # Send request to Alpha Vantage
        avRequest = requests.get(avEndpoint)
        # Raise any HTTP errors 
        avRequest.raise_for_status()
        # Access response data
        newsData = avRequest.json()
    
        # Try to access news feed data from response 
        try:
            newsFeed = newsData['feed']
        # Will be thrown if 'feed' wasn't in response (which contains the news storeis)
        except KeyError:
            print("ERROR: No news feed data found in the response")
            return False
        
        # Extract the publish time and sentiment of news stories from response 
        extractedData = []
        for story in newsFeed:
            # Extract publish date
            timePublished = story.get('time_published', 'N/A')
            if timePublished != 'N/A':
                # Convert date into format YYYY-MM-DD (same format as dates in stock price dataset)
                timePublishedObj = datetime.datetime.strptime(timePublished, "%Y%m%dT%H%M%S")
                timePublishedFormat = timePublishedObj.strftime("%Y-%m-%d")
            else:
                timePublishedFormat = 'N/A'

            extractedData.append({
                'time_published': timePublishedFormat,  
                'overall_sentiment_score': float(story.get('overall_sentiment_score', 0))
            }) 

        dfDescending = pd.DataFrame(extractedData)
        # Dataframe currently ordered in descennding order of date, need to reverse it so it's in ascending order 
        df = dfDescending.iloc[::-1]
        # print(df)

        # Get date where atleast 10 articles have been published on/before it (so we can properly calculate average)
        # Can simply just access 10th news story in extracted_data dataframe since it's ordered by date 
        earliestDate = df.iloc[9]['time_published']

        # Create a date range from the earliest date with at least 10 articles (to ensure all sentiment scores in dataset are calulated the same way/average of 10 scores)
        # Date range also ensures there will be an entry for every date (even if a news story wasn't published on that exact day)
        endDate = df.iloc[-1]['time_published']
        allDates = pd.date_range(start=earliestDate, end=endDate).strftime('%Y-%m-%d')

        # Initialize an empty dataframe to store average sentiment scores for valid dates
        sentimentDf = pd.DataFrame(allDates, columns=['time_published'])
        sentimentDf['average_sentiment_score'] = None

        # Calculate the average sentiment score for the 10 nearest dates for each valid date
        for currentDate in sentimentDf['time_published']:
            filteredDf = df[df['time_published'] <= currentDate]
            # If there are more than 10 entries selected, filter down to only include the 10 most recent ones
            if filteredDf.shape[0] >= 10:
                # Entries are in ascending order, so the 10 tail elements will be the most recent
                nearestDatesDf = filteredDf.tail(10)
                # Store average of these 10 sentiment scores 
                averageScore = nearestDatesDf['overall_sentiment_score'].mean()
                sentimentDf.loc[sentimentDf['time_published'] == currentDate, 'average_sentiment_score'] = averageScore


        # Save the dataframe as a csv file 
        csvFilename = f"{ticker}_sentimentDataset.csv"
        sentimentDf.to_csv(csvFilename, index=False)
        print(f"News sentiment average data saved to {csvFilename}")   
        return True 
    
    # Will be thrown if actual api request fails
    except requests.RequestException as e:
        print(f"HTTP request error: {e}")
        return False
    except ValueError as e:
        print(f"JSON parsing error: {e}")
        return False
    


# Used to ensure stock and sentiment datasets are the same shape
# Removes any sentiment entries for days where market is closed 
# Truncates stock dataset as it includes entries for more days 
def resizeDatasets() -> bool:
    try:

        # First need to reshape datasets to only include rows where the date/timestamp field is found in both datasets
        
        # Read current un-cleaned data
        stockDataframe = pd.read_csv('HSBC_stockDataset.csv')
        sentimentDataframe = pd.read_csv('HSBC_sentimentDataset.csv')

        # print(sentimentDataframe)

        # Find the intersection of dates present in both datasets
        common_dates = pd.Series(list(set(stockDataframe[stockDataframe.columns[0]]).intersection(set(sentimentDataframe[sentimentDataframe.columns[0]]))))

        # Filter both datasets to include only the common dates
        filterStockDataframe = stockDataframe[stockDataframe[stockDataframe.columns[0]].isin(common_dates)]
        filterSentimentDataframe = sentimentDataframe[sentimentDataframe[sentimentDataframe.columns[0]].isin(common_dates)]

        # Need to rename first column as it's currently 'Unnamed: 0' 
        filterStockDataframe.rename(columns = {'Unnamed: 0':'Date'}, inplace = True)

        # print(filterStockDataframe)
        # print(filterSentimentDataframe)


        # Now, need to get datasets into the correct format (each row is made up of previous 5 days data)



        # Store the prepared datasets (with no indexes)
        filterStockDataframe.to_csv('Clean_HSBC_stockDataset.csv', index=False)
        filterSentimentDataframe.to_csv('Clean_HSBC_sentimentDataset.csv', index=False)
    
        return True
    
    except Exception as e:
        print(f"ERROR: {e}", file=stderr)
        return False

    


if __name__ == "__main__":

    downloadStockData(ticker="HSBA.LON", outputsize="full")
    downloadNewsSentiment(ticker="HSBC", time_from="20220222T0000", limit=1000)
    resizeDatasets()
