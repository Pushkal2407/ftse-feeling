import React from 'react';
import './navbar.css';
import logo from '../../assets/ftse-logo.png';
import { Link } from 'react-router-dom';


import axios from "axios";
import {
  createBrowserRouter,  RouterProvider,
  useNavigate
} from "react-router-dom";



const Navbar = () => {
  const navigate = useNavigate();



  const handleLogout = async (event) => {
      const confirmed = window.confirm("Are you sure you want to logout?");
    event.preventDefault();
    if(confirmed){

      try {
          const response = await axios.post('http://127.0.0.1:5000/logout'); // Sending logout request to flask server 
  
          console.log(response.data)
          if (response.data =="success"){
              localStorage.clear();
              sessionStorage.clear();
              navigate('/Login') ; // Navigating to Login page after successful logout
  
          }
  
  
  
      } catch (error) {
          console.error('logout failed:', error.message);
      }
    }
  };



  return (
    <nav className='navbar'>
        <Link to='/HomePage'>
        <img src={logo} alt="Logo" className='logo'/>
        </Link>


        
        
        <div className='BrowseNProfile'>
        <button className='LogoutButton' onClick={handleLogout}> Log out </button>
        <Link to ='/BrowsePage'>
        <button className='BrowseProfileButton'>   
        <span className="Browse-content">Browse</span>
        </button>
        </Link>

        <Link to ='/ProfilePage'>
        <button className='BrowseProfileButton'>   
        <svg className='Browsecontent' xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-fill" viewBox="0 0 16 16">
            <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6"/>
        </svg>
        </button>
        </Link>

        </div>
    </nav>
  )
}

export default Navbar