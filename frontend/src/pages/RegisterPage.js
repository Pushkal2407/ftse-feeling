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


import { GoogleLogin, useGoogleLogin } from '@react-oauth/google';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { jwtDecode } from "jwt-decode"; //to decode the credentials
import { UseGoogleLogin } from '@react-oauth/google';
import axios from "axios";
import Alert from '@mui/material/Alert';
import Stack from '@mui/material/Stack'; 




const RegisterPage = () => {
  const [email,setEmail] = useState('');
  const [confirmEmail,setConfirmEmail] = useState('');
  const [password,setPassword] = useState('');
  const [confirmPassword,setConfirmPassword] = useState('');
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState('');

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    confirmEmail: '',
    password: '',
    confirmPassword: ''
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:5000/register', formData);

      console.log(response.data)
      if (response.data =="success"){
        try {
          await axios.get('http://127.0.0.1:5000/sendVerification');
        }
        catch (error) {
          console.log(error);
        }
        navigate('/VerificationPage') ;
      }

      else {

        setErrorMessage(response.data);

        return <h1>response.data</h1> ///////////////////// need a red banner simply displaying the text in response.data
      }


    } catch (error) {
      console.error('Registration failed:', error.message);
    }
  };
  







  return (
    <div className='LoginPage'>
      <img src={logo} alt="Logo" className='logo'/>
    <div className='card-container'>
    <div className='card'>
     <div className="card2">
    <form className="form" onSubmit={handleSubmit}>
      <p className="heading">Register</p>
      <div className="field">
      <svg className="input-icon" xmlns="http://www.w3.org/2000/svg"  width="16" height="16" fill="#2e2e2e" viewBox="0 0 448 512">
            <path d="M224 256c70.7 0 128-57.31 128-128s-57.3-128-128-128C153.3 0 96 57.31 96 128S153.3 256 224 256zM274.7 304H173.3C77.61 304 0 381.6 0 477.3c0 19.14 15.52 34.67 34.66 34.67h378.7C432.5 512 448 496.5 448 477.3C448 381.6 370.4 304 274.7 304z"></path>
            </svg>
          <input className="input-field" type="text" name="name" value={formData.name} onChange={handleInputChange} placeholder="Name" required /> </div>
          <div className="field">
          <svg className="input-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#2e2e2e" viewBox="0 0 16 16">
            <path d="M13.106 7.222c0-2.967-2.249-5.032-5.482-5.032-3.35 0-5.646 2.318-5.646 5.702 0 3.493 2.235 5.708 5.762 5.708.862 0 1.689-.123 2.304-.335v-.862c-.43.199-1.354.328-2.29.328-2.926 0-4.813-1.88-4.813-4.798 0-2.844 1.921-4.881 4.594-4.881 2.735 0 4.608 1.688 4.608 4.156 0 1.682-.554 2.769-1.416 2.769-.492 0-.772-.28-.772-.76V5.206H8.923v.834h-.11c-.266-.595-.881-.964-1.6-.964-1.4 0-2.378 1.162-2.378 2.823 0 1.737.957 2.906 2.379 2.906.8 0 1.415-.39 1.709-1.087h.11c.081.67.703 1.148 1.503 1.148 1.572 0 2.57-1.415 2.57-3.643zm-7.177.704c0-1.197.54-1.907 1.456-1.907.93 0 1.524.738 1.524 1.907S8.308 9.84 7.371 9.84c-.895 0-1.442-.725-1.442-1.914z"></path>
        </svg>
          <input className="input-field" type="email" name="email" value={formData.email} onChange={handleInputChange} placeholder="Email" required />
          </div>
          <div className="field">
          <svg className="input-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#2e2e2e" viewBox="0 0 16 16">
            <path d="M13.106 7.222c0-2.967-2.249-5.032-5.482-5.032-3.35 0-5.646 2.318-5.646 5.702 0 3.493 2.235 5.708 5.762 5.708.862 0 1.689-.123 2.304-.335v-.862c-.43.199-1.354.328-2.29.328-2.926 0-4.813-1.88-4.813-4.798 0-2.844 1.921-4.881 4.594-4.881 2.735 0 4.608 1.688 4.608 4.156 0 1.682-.554 2.769-1.416 2.769-.492 0-.772-.28-.772-.76V5.206H8.923v.834h-.11c-.266-.595-.881-.964-1.6-.964-1.4 0-2.378 1.162-2.378 2.823 0 1.737.957 2.906 2.379 2.906.8 0 1.415-.39 1.709-1.087h.11c.081.67.703 1.148 1.503 1.148 1.572 0 2.57-1.415 2.57-3.643zm-7.177.704c0-1.197.54-1.907 1.456-1.907.93 0 1.524.738 1.524 1.907S8.308 9.84 7.371 9.84c-.895 0-1.442-.725-1.442-1.914z"></path>
        </svg>
          <input className="input-field" type="email" name="confirmEmail" value={formData.confirmEmail} onChange={handleInputChange} placeholder="Confirm Email" required />
          </div>
          <div className="field">
          <svg className="input-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#2e2e2e" viewBox="0 0 16 16">
    <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"></path>
    </svg>
          <input className="input-field" type="password" name="password" value={formData.password} onChange={handleInputChange} placeholder="Password" required /> </div>
          <div className="field">
          <svg className="input-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#2e2e2e" viewBox="0 0 16 16">
    <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"></path>
    </svg>

          <input className="input-field" type="password" name="confirmPassword" value={formData.confirmPassword} onChange={handleInputChange} placeholder="Confirm Password" required /> </div>
          {/* <Link to='/SendVerificationPage'> */}

          <button id = "button1" className="button" type="submit" onClick={handleSubmit}>Register</button>
          {/* </Link> */}
          <p className="text">Already have an account?<Link to="/Login" id="register-link">Login</Link></p>
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



export default RegisterPage;