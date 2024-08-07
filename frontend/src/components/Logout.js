import React from 'react';
import './Logout.css';
import httpClient from './httpClient.js';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  RouterProvider,
  useNavigate
} from "react-router-dom";
import App from './App.jsx';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import logo from '../assets/ftse-logo.png';
import axios from "axios";




const Logout= () => {
    const navigate = useNavigate();


    const handleSubmit = async (event) => {
    const confirmed = window.confirm("Are you sure you want to logout?");
      event.preventDefault();
      if(confirmed){
  
        try {
            const response = await axios.post('http://127.0.0.1:5000/logout');
            
            console.log(response.data)
            if (response.data =="success"){
                localStorage.clear();
                sessionStorage.clear();
                navigate('/Login') ;
    
            }
        } catch (error) {
            console.error('logout failed:', error.message);
        }
      }
    };


 

  

    return (
      <div className="button-choose">
        <img src={logo} alt="Logo" className='logo'/>
        <button
        id="button1"
        onClick={handleSubmit}
      >
        Log out
      </button>
    </div>

    );
};
    

export default Logout;