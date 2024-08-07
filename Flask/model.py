import numpy as np 
import pandas as pd 
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
import tensorflow as tf
import datetime
from os import getenv
import requests 
from sys import stderr
from typing import Tuple

# Configuration for model and data processing
modelConfig = {
    "splitPercentage": 90,  # train/test dataset split, 90% for training, 10% for testing
    "numInputDays": 1,  # How many previous days stock/sentiment data are considered when making prediction 
    "numEpochs": 100,
    "alpha": 0.04,  # Adjusts the model's learning rate
    "paths": {
        "stock": "Clean_HSBC_stockDataset.csv",
        "sentiment": "Clean_HSBC_sentimentDataset.csv",
    },
    "columns": {
        "stock": ["Close"],
        "sentiment": ["average_sentiment_score"],
    },
}

# Load datasets
def loadData(filePath, columns):
    return pd.read_csv(filePath, usecols=columns)

stockData = loadData(modelConfig["paths"]["stock"], modelConfig["columns"]["stock"])
sentimentData = loadData(modelConfig["paths"]["sentiment"], modelConfig["columns"]["sentiment"])

# Determine the size of the training set
def computeSplitIndex(dataLength, percentage):
    return int(dataLength * (percentage / 100.0))

splitIndex = computeSplitIndex(stockData.shape[0], modelConfig["splitPercentage"])

# Apply MinMax scaling to normalize the data
normScaler = MinMaxScaler()
normalizedStocks = normScaler.fit_transform(stockData)
normalizedSentiments = normScaler.fit_transform(sentimentData)

# Generate sequences for model input
def createSequences(data, sentimentScores, sequenceLength, startIndex):
    sequences, sentiments, targets = [], [], []
    for i in range(startIndex, len(data) - sequenceLength):
        sequences.append(data[i:i + sequenceLength])
        sentiments.append(sentimentScores[i + sequenceLength - 1])
        targets.append(data[i + sequenceLength])
    return np.array(sequences), np.array(sentiments), np.array(targets)

trainSequences, trainSentiments, trainTargets = createSequences(
    normalizedStocks[:splitIndex],
    normalizedSentiments[:splitIndex],
    modelConfig["numInputDays"],
    0,
)

testSequences, testSentiments, testTargets = createSequences(
    normalizedStocks[splitIndex:],
    normalizedSentiments[splitIndex:],
    modelConfig["numInputDays"],
    0,
)

# Incorporate sentiment data into sequences
def appendSentimentToSequences(sequences, sentiments):
    return np.array([np.append(seq, sentiment) for seq, sentiment in zip(sequences, sentiments)])

trainData = appendSentimentToSequences(trainSequences, trainSentiments)
testData = appendSentimentToSequences(testSequences, testSentiments)

# Set up the LSTM Model 
def setupModel(seed:int=1):
    # Set seed, so that the initialisation values of variables can be reproduced across runs 
    tf.random.set_seed(seed)
    model = tf.keras.models.Sequential(
        [
            tf.keras.Input(shape = (trainData.shape[1], 1)),
            tf.keras.layers.LSTM(units = 64, activation = "tanh", return_sequences = True),
            tf.keras.layers.LSTM(units = 32, activation = "tanh", return_sequences = True),
            tf.keras.layers.LSTM(units = 16, activation = "tanh", return_sequences = False),
            tf.keras.layers.Dense(units = 1, activation = "linear") # Outputs Closing price for next day 
        ]   
    )

    model.compile(
        loss = tf.keras.losses.mean_squared_error,
        optimizer = tf.keras.optimizers.Adam(learning_rate = modelConfig['alpha'])
    )

    model.fit(
        trainData, trainTargets,
        epochs = modelConfig['numEpochs']
    )
    return model


# inverting normalistion
y_test = normScaler.inverse_transform(testTargets)



# Get predictions for test dataset
def predict(model):
    predictions = model.predict(testData)
    predictions = normScaler.inverse_transform(predictions.reshape(-1,1)).reshape(-1,1)
    return predictions




# Evaluate the trained model
def evaluate(predictions) -> Tuple[float, float, float]:
    mae = mean_absolute_error(predictions, y_test)
    mape = mean_absolute_percentage_error(predictions, y_test)
    return mae, mape, (1 - mape) # 1- mean absolute percentage error = accuracy of model

# Load trained model 
def loadModel(filepath:str="trainedModel.keras"):
    try:
        model = tf.keras.models.load_model(filepath)
        return model 
    # If model file doesn't exist 
    except: 
        return False

    

# Train and save the model, then return performance metrics 
def train() -> Tuple[float, float, float] :    
    model = setupModel()
    model.save("trainedModel.keras")
    predictions = predict(model)
    # mae = mean absolute error
    # mape = mean absolute percentage error
    # accuracy = 1 - mape 
    mae, mape, accuracy = evaluate(predictions)
    return mae, mape, accuracy

def make_prediction(ticker:str):

    # Fetch API key from environment variable AV_KEY
    avKey = getenv('AV_KEY')
    # If AV_KEY not set, getenv will return None 
    if not avKey:
        print("ERROR: Please store Alpha Vantage API Key in environment variable 'AV_KEY'")
        return None

    
    # Alpha Vantage endpoint for news and sentiment, will return 50 most recent (can't make it any smaller )
    avEndpoint = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={avKey}'

    try:
        # Send request to Alpha Vantage
        avRequest = requests.get(avEndpoint)
        # Raise any HTTP errors 
        avRequest.raise_for_status()
        # Access response data
        newsData = avRequest.json()
        # print(newsData)
        # Try to access news feed data from response 
        try:
            newsFeed = newsData['feed']
            # print(newsFeed)
            # Find average sentiment for the first 10 sentiment scores 
            sentimentTotal = 0.0
            for i, sentimentScore in enumerate(newsFeed):
                # Only want to find average of 10 articles (loop is 0-indexed)
                if i>9:
                    break
                sentimentTotal += float(sentimentScore['overall_sentiment_score'])

            # Divide by i to find average, since there may have been less than 10 (store in list as needed by model)
            averageSentiment = float(sentimentTotal/i)

            # print(averageSentiment)

            # Get OHCLV market data from previous day 
            # Alpha Vantage endpoint for daily OHCLV stock data
            avEndpoint = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=HSBA.LON&apikey={avKey}'

            # Send request for stock data from AlphaVantage
            avRequest = requests.get(avEndpoint)
            # Raises HTTPError for bad responses
            avRequest.raise_for_status()  
            # Access response data
            stockData = avRequest.json()
            # print(stockData)

            previousDayData = list(stockData['Time Series (Daily)'].values())[0]
            # print(previousDayData)

            previousClose = float(previousDayData['4. close'])

            # print(stockData)
            # print(previousDayData)
            # print(previousClose)
            # Check that API didn't return an error message
            if "Error Message" in stockData:
                print("ERROR: Failed to fetch data. Please check API key and Ticker symbol.", file=stderr)
                return None
            

            
            # Now need to pass average sentiment and price data into LSTM to get prediction     

            # First load trained model (if it exists, otherwise need to train)
            trainedModel = loadModel()
            if not trainedModel:
                print("ERROR: Trained model not found, please call run_model() function then try again", file=stderr)
                return None
        
            # Now make prediction
            # Need to combine sentiment and price data into single array
            
            # Convert lists to np arrays (same format as data used when training)
            closingPriceArray = np.array(previousClose).reshape(-1, 1)  
            sentimentScoreArray = np.array(averageSentiment).reshape(-1, 1)  
            
            # Normalise data (this was done to the training data, so must be done here as well)
            normScaler = MinMaxScaler().fit(closingPriceArray) 
            closingPriceNormalised = normScaler.transform(closingPriceArray)[0][0]
            # print(closingPriceNormalised)

            # Preparing sequences for the model
            predictionInput = np.array([[[closingPriceNormalised], [averageSentiment]]]).reshape(1,2,1)
            
            # Get the prediction
            prediction = trainedModel.predict(predictionInput)
            # Call inverse normalisation function on prediction (i.e. get the actual prediction value)
            prediction = normScaler.inverse_transform(prediction.reshape(-1,1)).reshape(-1,1)
            # Return predicted closing price 
            return prediction[0][0]
            
            
        # Will be thrown if 'feed' wasn't in response (which contains the news storeis)
        except KeyError:
            print("ERROR: No news feed data found in the response")
            return False

        

    # Will be thrown if actual api request fails
    except requests.RequestException as e:
        print(f"HTTP request error: {e}")
        return False 


# mae, mape, accuracy = train()
# print(mae)
# print(mape)
# print(accuracy)


print(make_prediction("HSBC"))
#print("Predicted Value for HSBA.LON: 579.9544")