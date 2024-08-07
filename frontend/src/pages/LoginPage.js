import React from 'react';
import './LoginPage.css';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  RouterProvider,
  useNavigate
} from "react-router-dom";
import App from './App.jsx';
import { useEffect, useState } from 'react';

import { GoogleLogin, useGoogleLogin } from '@react-oauth/google';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { jwtDecode } from "jwt-decode"; //to decode the credentials
import { UseGoogleLogin } from '@react-oauth/google';
import axios from "axios";




// main function
const LoginPage = () => {

  const navigate = useNavigate();
  // sets up consts for data
  const [formData, setFormData] = useState({
    email: '',
    password: ''
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
      console.log(formData)
      const response = await axios.post('http://127.0.0.1:5000/login', formData);
      console.log(response);
      // navigate("/HomePage");

      if (!response.ok) {
        throw new Error('Failed to login');
      }

      // Handle success response
      console.log('Login successful');
    } catch (error) {
      // Handle error here, e.g., show an error message
      console.error('Login failed:', error.message);
    }
  };






  return (
    <div class="wrapper">
    <h1>Login</h1>
    <div class="card-switch">
      <label class="switch">
          <input type="checkbox" class="toggle" />
        <span class="slider"></span>
        <span class="card-side"></span>
        <div class="flip-card__inner">
          <div class="flip-card__front"></div>
            <div class="title">Log in</div>
            <form class="flip-card__form" onSubmit={handleSubmit}>
              <input class="flip-card__input" name="email" placeholder="Email" type="email" value={formData.email} onChange={handleInputChange} required />
              <input class="flip-card__input" name="password" placeholder="Password" type="password" value={formData.password} onChange={handleInputChange} required/>
              <button class="flip-card__btn">Login</button>
              <GoogleOAuthProvider clientId="66939333394-ip11j96cou9h7dpf3u89rkdmqcrj6ob3.apps.googleusercontent.com">
              {/* <GoogleLogin {...googleLogin} /> */}
            </GoogleOAuthProvider>
            </form>
            </div>
        </label>  
      </div>

      </div>
  );
};

export default LoginPage;
