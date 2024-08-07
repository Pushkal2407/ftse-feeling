import React from 'react';
import './LoginPage.css';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  Link,
  RouterProvider,
  useNavigate
} from "react-router-dom";
import App from './App.jsx';
import { useEffect, useState } from 'react';


import logo from '../assets/ftse-logo.png';
import axios from "axios";
import Alert from '@mui/material/Alert';
import Stack from '@mui/material/Stack'; 






const Login= () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
      email: '',
      password: '',
    });

    const handleInputChange = (event) => {
      const { name, value } = event.target;
      setFormData({
        ...formData,
        [name]: value
      });

      if (name === "email") {
        setEmail(value);
      } else if (name === "password") {
        setPassword(value);
      }
    };


    const handleSubmit = async (event) => {
      event.preventDefault();
  
      try {
        const response = await axios.post('http://127.0.0.1:5000/login', formData);
  
        console.log(response.data)
        if (response.data =="success"){
          navigate('/HomePage') ;
  
        } else{

          setErrorMessage("Wrong email or password");
        }
  
  
  
      } catch (error) {
        console.error('login failed:', error.message);
      }
    };

    const resetPassword = async (event) => {
      event.preventDefault();
  
      try {
          navigate('/PasswordResetPage') ;
  
      } catch (error) {
        console.error('login failed:', error.message);
      }
    };

  


    return (
      <div className='LoginPage'>
        <img src={logo} alt="Logo" className='logo'/>
      <div className='card-container'>
      <div className='card'>
        <div className="card2">
      <form className="form" onSubmit={handleSubmit}>
        <p className="heading">Login</p>
        <div className="field">
        <svg className="input-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#2e2e2e" viewBox="0 0 16 16">
            <path d="M13.106 7.222c0-2.967-2.249-5.032-5.482-5.032-3.35 0-5.646 2.318-5.646 5.702 0 3.493 2.235 5.708 5.762 5.708.862 0 1.689-.123 2.304-.335v-.862c-.43.199-1.354.328-2.29.328-2.926 0-4.813-1.88-4.813-4.798 0-2.844 1.921-4.881 4.594-4.881 2.735 0 4.608 1.688 4.608 4.156 0 1.682-.554 2.769-1.416 2.769-.492 0-.772-.28-.772-.76V5.206H8.923v.834h-.11c-.266-.595-.881-.964-1.6-.964-1.4 0-2.378 1.162-2.378 2.823 0 1.737.957 2.906 2.379 2.906.8 0 1.415-.39 1.709-1.087h.11c.081.67.703 1.148 1.503 1.148 1.572 0 2.57-1.415 2.57-3.643zm-7.177.704c0-1.197.54-1.907 1.456-1.907.93 0 1.524.738 1.524 1.907S8.308 9.84 7.371 9.84c-.895 0-1.442-.725-1.442-1.914z"></path>
        </svg>
      <input name = "email" type="email" className="input-field" id="username" placeholder="Email" value={email}
                      onChange={handleInputChange}
                      required/>
      </div>
      <div className="field">
    <svg className="input-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#2e2e2e" viewBox="0 0 16 16">
    <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"></path>
    </svg>
                    <input
                      className="input-field"
                      id="password"
                      name="password"
                      placeholder="Password"
                      type="password"
                      value={password}
                      onChange={handleInputChange}
                      required
                    />
                    </div>
                    <button id = "button1"
                      type="button"
                      className="button"
                      onClick={handleSubmit}
                    >
                      Login
                    </button>
                    <div>
                   
                    <button id = "button1" className="button" onClick = {resetPassword}>Forgot your password?</button>
                    </div>
                    <p className="text">Don't have an account? <Link to="/RegisterPage" className="register-link">Register</Link></p>
                    {errorMessage && (
        <Stack sx={{ width: '100%' }} spacing={2}>
          <Alert severity="error">{errorMessage}</Alert>
        </Stack>
      )}
                    </form>
                    </div>
                    </div>
                    </div>
                    </div>









  );
  
};


export default Login