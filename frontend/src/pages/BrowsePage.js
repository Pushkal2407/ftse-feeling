import React, { useState, useEffect} from 'react';
import Navbar from '../components/NavBar/navbar'
import './BrowsePage.css'
import { Link } from 'react-router-dom';

// Function to fetch all companies data
async function getAllComps() {

    try {
      let response = await fetch('http://127.0.0.1:5000/getCompaniesData');
      let responseJson = await response.json();
      return responseJson.data;
     } catch(error) {   
      console.error(error);
    }
}

// Browse Page component
const BrowsePage = () => {
    const [Companies, setCompanies] = useState([]);
    useEffect(() => {

        async function fetchCompanies() {

            const comps = await getAllComps();
       
            setCompanies(comps);
        }
        fetchCompanies();
    }, []);
  return (

    <div className='BrowsePage'>
            <Navbar />
            <h1>Browse</h1>
            <div className="Bcontainer">
                <div className="Bgrid">
                    {Companies.map((item, index) => (
                        <Link to ={`/CompanyPage?name=${item[0]}`}>
                        <button className='Bbutton' key={index}>
                        <div className='Bimage-container'>
                            {item[3 ] && <img className='Blogo' src={item[3]} alt={item[1]} />}
                        </div>
                        <div className='Bcontent'>
                        <h3>{item[1]}</h3>
                        </div>
                        </button>
                        </Link>
                    ))}
                </div>
            </div>
        </div>
  )
}

export default BrowsePage