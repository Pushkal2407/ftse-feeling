import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
// import App from './App';
import HomePage from './pages/HomePage';
import BrowsePage from './pages/BrowsePage';
import ProfilePage from './pages/ProfilePage';
import CompanyPage from './pages/CompanyPage';
import LoginPage  from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Login from './pages/Login';
import { GoogleOAuthProvider } from '@react-oauth/google';
import App from "./App.jsx";
import cors from 'cors';
import Verification from './pages/Verification';

import SendVerification from './pages/SendVerification';
import PasswordResetPage from './pages/PasswordResetPage';


import PasswordResetCodePage from './pages/PasswordResetCodePage';
import DesktopNotification from './components/DesktopNotification';




// const express = require('express');
// const app = express(); // Define app as an instance of Express.js

// Import and use cors middleware
// app.use(cors({
//   origin: 'http://localhost:3000/',
//   methods: ['GET', 'POST']
// }));


const router = createBrowserRouter([
  {
    path: "HomePage",
    element: <HomePage/>,
  },
  {
    path: "BrowsePage",
    element: <BrowsePage/>
  },
  {
    path: "ProfilePage",
    element: <ProfilePage/>
  },
  {
    path: "CompanyPage",
    element: <CompanyPage/>
  },
  {
    path: "LoginPage",
    element: <LoginPage/>
  },
  {
    path: "Login",
    element: <Login/>
  },
  {
    path: "RegisterPage",
    element: <RegisterPage/>
  },

  {
    path: "VerificationPage",
    element: <Verification/>
  },
  {

    path: "SendVerificationPage",
    element: <SendVerification/>

  },
  {
    path: "PasswordResetPage",
    element: <PasswordResetPage/>
  },

  {
    path: "PasswordResetPage",
    element: <PasswordResetPage/>
  },
  {
    path: "PasswordResetCodePage",
    element: <PasswordResetCodePage/>
  },
  {
    path: "DesktopNotification",
    element: <DesktopNotification/>
  }

  



]);




const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
    <GoogleOAuthProvider clientId= "66939333394-ip11j96cou9h7dpf3u89rkdmqcrj6ob3.apps.googleusercontent.com">
    
      <App />
    </GoogleOAuthProvider>
     
  </React.StrictMode>
);

