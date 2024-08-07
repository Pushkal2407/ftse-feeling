import React, { useState } from 'react'; // Importing necessary modules from React
import { useNavigate } from "react-router-dom"; // Importing useNavigate hook from React Router
import axios from "axios"; // Importing axios for HTTP requests
import logo from '../assets/ftse-logo.png'; // Importing logo image
import './LoginPage.css'; // Importing styles for LoginPage

// PasswordResetCodePage component
const PasswordResetCodePage = () => {
  const [code, setCode] = useState(''); // State for code
  const [password, setPassword] = useState(''); // State for password
  const navigate = useNavigate(); // Hook for navigation

  const [formData, setFormData] = useState({ // State for form data
    code: '',
    password: '',
  });

  // Function to handle input change
  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  // Function to handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const resp = await axios.post('http://127.0.0.1:5000/checkPasswordCode', formData); // Sending POST request to check password code
      console.log(resp.data);
      if (resp.data === "success") {
        navigate('/Login'); // Navigate to Login page on success
      }
    } catch (error) {
      console.error('Password reset failed:', error.message);
    }
  };

  // Rendering JSX
  return (
    <div className='LoginPage'>
      <img src={logo} alt="Logo" className='logo'/>
      <div className='card-container'>
        <div className='card'>
          <div className="card2">
            <form className="form" onSubmit={handleSubmit}>
              <p className="heading">Password Reset</p>
              <p>A code verifying your identity should have been sent to your email. Please enter it below. If it hasn't arrived yet, wait 30 seconds and then <u>resend</u></p>
              <div className="field">
                <input className="input-field" type="number" name="code" value={formData.code} onChange={handleInputChange} placeholder="xxxxxx" maxLength="6" minLength="6" required />
              </div>
              <div className="field">
                <svg className="input-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#2e2e2e" viewBox="0 0 16 16">
                  <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"></path>
                </svg>
                <input className="input-field" type="password" name="password" value={formData.password} onChange={handleInputChange} placeholder="Password" required />
              </div>
              <button id="button1" className="button" type="submit" onClick={handleSubmit}>Reset</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PasswordResetCodePage; // Exporting PasswordResetCodePage component
