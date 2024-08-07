import React, { useState, useEffect } from 'react';
import './NewsButton.css';
import DropdownFilter from './DropdownFilter';

async function getNewsFromApi(ticker) {
  try {
    let response = await fetch('https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=' + ticker + '&sort=RELEVANCE&LIMIT=5&apikey=UGACXLHBY5FDJCEW');
    let responseJson = await response.json();
    // console.log(responseJson)
    return responseJson.feed;
  } catch (error) {
    console.error(error);
  }
}

async function getFollowedTickers() {
  try {
    let response = await fetch('http://127.0.0.1:5000/getFollowed');
    let responseJson = await response.json();
    // console.log(responseJson)
    return responseJson.data;
  } catch (error) {
    console.error(error);
  }
}


function NewsButton() {
  const [newsData, setNewsData] = useState([]);

  useEffect(() => {
    // Fetch news data when component mounts
    async function fetchNews() {
      const tickerList = await getFollowedTickers();
      let tickers=[];
      
      for (let i = 0; i < tickerList.length; i++) {
        tickers.push(tickerList[i][1])

      }

      var returnFeed;
      if (tickers.length ==0){
        var news = await getNewsFromApi("");

      }
      for (let i = 0; i < tickers.length; i++){
        let ticker = tickers[i]

        var news = await getNewsFromApi(ticker);
        returnFeed = Object.assign({},returnFeed, news);

    }

  let stories=[];

  for (var i in returnFeed){
    stories.push(returnFeed[i])

  }
    setNewsData(stories); // Updating 'newsData' state with fetched news stories
    }
    fetchNews();
  }, []);

  return (
    <div className="container">
      <div className="grid">
        <DropdownFilter className='filter-button'></DropdownFilter>
        {newsData.map((article, index) => (
          <a href={article.url} target='_blank' key={index}>
            <button className='Nbutton'>
              <div className='Nimage-container'>
                <img src={article.banner_image} alt={article.title}/>
                <span className='sentiment-container'>Sentiment Score: <span className={getClassForSentiment(article.overall_sentiment_score)}>{article.overall_sentiment_score}</span></span>
              </div>
              <div className='Ncontent'>
                <h3>{article.title}</h3>
                <p>{article.summary}</p>
              </div>
            </button>
          </a>
        ))}
      </div>
    </div>
  );
}
// Function to determine CSS class based on sentiment score- negative sentiment score displayed in red and positive sentiment score displayed in green
function getClassForSentiment(sentimentScore) {
  if (sentimentScore > 0) {
    return 'positive';
  } else {
    return 'negative';
  }
}

export default NewsButton;
