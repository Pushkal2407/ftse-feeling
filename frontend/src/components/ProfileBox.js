import React, { useState, useEffect} from 'react';
import './ProfileBox.css';
import './ProfileButton.css';

// Function to fetch followed companies from the server
async function getFollowedComp() {

  try {
    let response = await fetch('http://127.0.0.1:5000/getFollowed'); // Fetching followed companies data from the server
    let responseJson = await response.json();
    return responseJson.data;
   } catch(error) {   
    console.error(error);
  }

}

// Function to fetch recommended companies from the server
async function getRecComp() {

  try {
    let response = await fetch('http://127.0.0.1:5000/getRecommended'); // Fetching recommended companies data from the server
    let responseJson = await response.json();
    return responseJson.data;
   } catch(error) {   
    console.error(error);
  }

}


function ProfileBox() {
  const [followedComp, setFollowedComp] = useState([]);
    useEffect(() => {

        async function fetchFollowedComp() {

            const comps = await getFollowedComp();
       
            setFollowedComp(comps); // Updating 'followedComp' state with fetched data
        }
        fetchFollowedComp();
    }, []);

    const [recComp, setRecComp] = useState([]);
    useEffect(() => {

        async function fetchRecComp() {

            const comps = await getRecComp();
       
            setRecComp(comps);
        }
        fetchRecComp();
    }, []);


  return (
    <div className="Pcontainer">
      <div className="Pbox1">
      <h1 style={{ fontSize: '20px' }}>Followed Companies</h1>
        <ul className="button-choose">
        {followedComp.map((item, index) => (
        <li key={index}><button>{item[0]}</button></li> 
          ))}
        </ul>
      </div>
      
      <div className="Pbox2">
      <h1 style={{ fontSize: '20px' }}>Recommended Companies</h1>
        <ul className="button-choose">
        {recComp && recComp.length > 0 && recComp.map((item, index) => (
        <li key={index}><button>{item[0]}</button></li> 
      ))}
        </ul>
      </div>
      
      <div className='Pbox3'>
      <h1 style={{ fontSize: '20px' }}>NotificationInput</h1> 
      </div>
      
      <div className='Pbox4'>
      <h1 style={{ fontSize: '20px' }}>ModelExplanation</h1>
      </div>
    </div>
  );
}

export default ProfileBox;
