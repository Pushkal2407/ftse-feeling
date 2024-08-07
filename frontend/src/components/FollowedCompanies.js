import React, { useState, useEffect} from 'react';
import './FollowedCompanies.css'
import { Link } from 'react-router-dom';






async function getFollowedComp() {

  try{
    let response = await fetch('http://127.0.0.1:5000/getFollowed');
    let responseJson = await response.json();
    console.log(responseJson)
    return responseJson.data;
  }catch(error) {   
    console.error(error);
  }

}





const FollowedCompanies = () => {
  const [followedComp, setFollowedComp] = useState([]); // Initializing state variable 'followedComp' with empty array
    useEffect(() => { // useEffect hook to fetch followed companies data when the component mounts

        async function fetchFollowedComp() {

            const comps = await getFollowedComp(); // Fetching followed companies data
            console.log(comps)
       
            setFollowedComp(comps); // Updating 'followedComp' state with fetched data
        }
        fetchFollowedComp();
    }, []); // Empty dependency array to run effect only once when the component mounts

      
  return (
 
    <div className="Followed-comp">
            <h2>Followed Companies</h2>
            <ul className="button-list">
                {followedComp.map((item, index) => (
                  <Link to ={`/CompanyPage?name=${item[1]}`}>
                    <li key={index}><button>{item[0]}</button></li> 
                  </Link>
                ))}
            </ul>
        </div>
       
  );
};

export default FollowedCompanies