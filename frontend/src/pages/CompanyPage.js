import React, { useState, useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import Navbar from '../components/NavBar/navbar';
import './CompanyPage.css';
import FollowButton from '../components/FollowButton';
import UnfollowButton from '../components/UnfollowButton';

function MyTick() {
    const queryParams = new URLSearchParams(window.location.search);
    const value = queryParams.get('name'); // Retrieve the value of a specific query parameter
    return value;
}


function follow_unfollow(ticker, comps) {
    var isF = false;

    // Check if ticker matches any item in comps
    comps.forEach(item => {
        if (ticker === item[1]) {
            isF = true;
        }
    });

    // Return UnfollowButton or FollowButton based on the value of isF
    if (isF) {
        return <UnfollowButton />;
    } else {
        return <FollowButton />;
    }
}
// Get news stories
async function getNewsFromApi(ticker) {
    try {
        let response = await fetch('https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers='+ticker+'&sort=RELEVANCE&LIMIT=5&apikey=UGACXLHBY5FDJCEW');
        let responseJson = await response.json();
        console.log(responseJson);
        return responseJson.feed;
    } catch(error) {   
        console.error(error);
    }
}

// get list of followed companies
async function getFollowedComp() {

    try {
      let response = await fetch('http://127.0.0.1:5000/getFollowed');
      let responseJson = await response.json();
      console.log(responseJson)
      return responseJson.data;
     } catch(error) {   
      console.error(error);
    }

}

// Get stock prediction
async function getPrediction(ticker) {

    try {
      let response = await fetch(`http://127.0.0.1:5000/getPrediction?ticker=${ticker}`);
      let responseJson = await response.json();
      console.log(responseJson)
      return responseJson.data;
     } catch(error) {   
      console.error(error);
    }

}


async function getGraphFromApi(ticker) {
    try {
        let response = await fetch(`http://127.0.0.1:5000/getGraphData?ticker=${ticker}`);
        let responseJson = await response.json();
        // console.log(responseJson)

        return responseJson;
    } catch(error) {   
        console.error(error);
    }
}

// Get a specific companies data
async function getCompData(ticker) {
    try {
        let response = await fetch(`http://127.0.0.1:5000/getCompanyData?ticker=${ticker}`);
        let responseJson = await response.json();
        return responseJson.data;
    } catch(error) {   
        console.error(error);
    }
}

// Get fundamental data about company
async function getFundementalData(ticker) {
    try {
        let response = await fetch(`http://127.0.0.1:5000/getFundementals?ticker=${ticker}`);
        let responseJson = await response.json();
        return responseJson.data;
    } catch(error) {   
        console.error(error);
    }
}

// Main company instance
const CompanyPage = () => {
    
    const chartRef = useRef(null);
    const chartInstance = useRef(null);

    const [followedComp, setFollowedComp] = useState([]);
    useEffect(() => {

        async function fetchFollowedComp() {

            const comps = await getFollowedComp();
            console.log(comps)
       
            setFollowedComp(comps);
        }
        fetchFollowedComp();
    }, []);



    useEffect(() => {
        async function fetchData() {
            const ticker = MyTick();
            const news = await getNewsFromApi(ticker);
            const comp = await getCompData(ticker);
            const fund = await getFundementalData(ticker);
            const graphData = await getGraphFromApi(ticker);
            setNewsData(news);
            setCompData(comp);
            setFundData(fund);
            drawChart(graphData);
        }
        fetchData();
    }, []);



    const drawChart = (graphData) => {
    console.log(graphData)
    const xValues = graphData.xValues;
    const yValues = graphData.yValues;
    const minY = Math.min(...yValues);
    const maxY = Math.max(...yValues);



    // Destroy existing chart if it exists
    if (chartInstance.current) {
        chartInstance.current.destroy();
    }

    chartInstance.current = new Chart('stockChart', {
        type: 'line',
        data: {
            labels: xValues,
            datasets: [{
                fill: false,
                lineTension: 1,
                backgroundColor: 'rgba(0,0,255,1.0)',
                borderColor: 'rgba(0,0,255,0.7)',
                data: yValues
            }]
        },
        options: {
            pointStyle :false,
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                  display: false
                }},
           
            scales: {
                x: {
                    title: {
                      display: true,
                      text: 'Date'
                    },
                    ticks:{stepSize:"01"}
                },
                y: {
                    title: {
                        display: true,
                        text: 'Stock Closing Price'
                    },
                    ticks: { min: minY, max: maxY }
                }
                
            }
        }
    });
    };

    const [newsData, setNewsData] = useState([]);
    useEffect(() => {
        // Fetch news data when component mounts
        async function fetchNews() {
            const ticker = MyTick(); 
            const news = await getNewsFromApi(ticker);
            setNewsData(news);
        }
        fetchNews();
    }, []);

    

    const [compData, setCompData] = useState([]);
    useEffect(() => {
        // Fetch news data when component mounts
        async function fetchCompData() {
            const ticker = MyTick(); 
            const data = await getCompData(ticker);
            setCompData(data);
        }
        fetchCompData();
    }, []);


    const [predicData, setPredicData] = useState([]);
    useEffect(() => {
        // Fetch news data when component mounts
        async function fetchPrediction() {
            const ticker = MyTick(); // change this as hard coded
            const data = await getPrediction(ticker);
            setPredicData(data);
        }
        fetchPrediction();
    }, []);


    const [fundData, setFundData] = useState([]);
    useEffect(() => {
        // Fetch news data when component mounts
        async function fetchFundData() {
            const ticker = MyTick(); // change this as hard coded
            const data = await getFundementalData(ticker);
            setFundData(data);
        }
        fetchFundData();
    }, []);


    // set up conts that can be used later
    const companyName = compData[0]; 
    const industry = compData[1]; 
    const ticker = compData[3]; 
    const companyOfficials = compData[4];
    const Complogo = compData[6];   
    const prediction = predicData;
    const reportDate = fundData[1];
    const revenueTTM = fundData[2];
    const netGrossProfit = fundData[3];
    const ebitda = fundData[4];




  // create jsx
  return (
    <div className='CompPage'>
            <Navbar />
            <div className='logo-text'>
                <img src={Complogo} alt='logo' className='CompLogo' />
                <h1 className='compText'>{companyName} ({ticker})</h1>
                <div className='sentimentBox'>{follow_unfollow(ticker, followedComp)}</div>
            </div>
            <div className='graph'>
                <canvas ref={chartRef} id="stockChart" style={{ width: '100%' }}></canvas>
            </div>
        
        <div className='NarticleAndData'>
            <div className='CNArticle'>
                <div className="Cgrid">
                   
                    {newsData.map((article, index) => (
                <a href={article.url} target='_blank'>
                    <button className='Nbutton' key={index}>
                        <div className='Nimage-container'>
                            <img src={article.banner_image} alt={article.title}/>
                            {article.topics.relevance_score}
                           

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
            <div className='Data'>
            <h2>Financial Data</h2>
            <ul>
                <li>
                    <strong>EBITDA:</strong> {ebitda}
                </li>
                <li>
                    <strong>Latest Quarter:</strong> {reportDate}
                </li>
                <li>
                    <strong>Revenue TTM:</strong> {revenueTTM}
                </li>
                <li>
                    <strong>Gross Profit TTM:</strong> {netGrossProfit}
                </li>
                <li>
                    <strong>Stock Prediction for next day:</strong> {prediction}
                </li>
            </ul>
        </div>
        </div>

      

    </div>
  )
}

export default CompanyPage
