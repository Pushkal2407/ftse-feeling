import React, { useState, useEffect } from 'react';
import './ProfileSidebar.css';
import profileImage from '../assets/profile.png';
import axios from 'axios';
import {
  createBrowserRouter,
  Link,
  RouterProvider,
  useNavigate
} from "react-router-dom";


const ProfileDetails = () => {
  const [userEmail, setUserEmail] = useState('');
  const [userInterests, setUserInterests] = useState('');
  const [userName, setUserName] = useState('');
  const userPassword = "***********"; 
  const [isPasswordEditable, setIsPasswordEditable] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    password: ''
  });
  const navigate = useNavigate();


  useEffect(() => {
    // Fetch user's details when component mounts
    fetchUserEmail();
    fetchUserInterest();
    fetchUserName();
  }, []);


  // Function to fetch user email from the server
  const fetchUserEmail = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/fetchEmail'); //fetching user data from the server
      console.log(response.data)
      setUserEmail(response.data.email); 
    } catch (error) {
      console.error('Failed to fetch user email:', error.message);
    }
  };

  // Function to fetch user interest from the server
  const fetchUserInterest = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/fetchInterest');
      console.log(response.data)
      setUserInterests(response.data.interest); 
    } catch (error) {
      console.error('Failed to fetch user interest:', error.message);
    }
  };

  // Function to fetch user's name from the server
  const fetchUserName = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/fetchName');
      console.log(response.data)
      setUserName(response.data.name); 
    } catch (error) {
      console.error('Failed to fetch user name:', error.message);
    }
  };


  

  // Function to handle input change in password field
  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  // Function to enable password change- only made true when change password button is clicked otherwise password field is not editable.
  const changePassword = () => {
    setIsPasswordEditable(true);
  };


  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/changePassword', formData);
      console.log(response.data);
      if (response.data === "success") {
        window.alert("Password changed successfully");
        setIsPasswordEditable(false); // Disable password input after successful change
        setFormData({ password: '' }); // Clear the newPassword field
      }
    } catch (error) {
      console.error('Password change failed:', error.message);
    }
  };



  return (
    <div className="profileDetailsSideBar">
      <img src={profileImage} alt="User Profile" style={{ maxWidth: '40%', height: 'auto' }} />
      <h2>{userName}</h2>
      <ul className="button-select">
          <li className="static-info">
              <span>Email:</span>
              <span>{userEmail}</span>
          </li>
          <li className="static-info">
              <span>Interests:</span>
              <span>{userInterests}</span>
          </li>

          <li className="static-info">
              <span>Password:</span>
              {isPasswordEditable ? (
            <input
            type={showPassword ? "text" : "password"}
            name="password"
            value={formData.password}
            onChange={handleInputChange}
          />
        ) : (
            <span>{userPassword}</span>
          )}
          </li>
          <li>
          <button onClick={() => setShowPassword(!showPassword)}>
            {showPassword ? "Hide Password" : "Show Password"}
          </button>
        </li>
          <li>
          <button onClick={changePassword}>Change Password</button>
          {isPasswordEditable && (
            <button onClick={handleSubmit}>Submit</button>
          )}
          </li>
      </ul>
    </div>
  );
}

export default ProfileDetails;

// added a different button- submit because otherwise clicking on change password makes the field editable but doesnt wait for user to enter new password but returns it was successful. 
