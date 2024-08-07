import React, { useState, useEffect} from 'react';
import './SuggestedCompanies.css'
import { Link } from 'react-router-dom';





// Function to fetch recommended companies from the server
async function getRecComp() {

    try {
      let response = await fetch('http://127.0.0.1:5000/getRecommended');
      let responseJson = await response.json();
      return responseJson.data;
     } catch(error) {   
      console.error(error);
    }

}


const SuggestedCompanies = () => {
  const [recComp, setRecComp] = useState([]);
    useEffect(() => {

        async function fetchRecComp() {

            const comps = await getRecComp();
       
            setRecComp(comps);
        }
        fetchRecComp();
    }, []);

      
  return (
 
    <div className="suggested-comp">
    <h2>Suggested Companies</h2>
    <ul className="button-list">
     
      {recComp && recComp.length > 0 && recComp.map((item, index) => (
        <Link to ={`/CompanyPage?name=${item[1]}`}>
          <li key={index}><button>{item[0]}</button></li> 
        </Link>
      ))}
    </ul>
  </div>
  );
};

export default SuggestedCompanies
