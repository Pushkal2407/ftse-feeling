import React, { useState } from 'react'; // Importing necessary modules from React
import { useNavigate } from "react-router-dom"; // Importing useNavigate hook from React Router
import axios from "axios"; // Importing axios for HTTP requests
import logo from '../assets/ftse-logo.png'; // Importing logo image
import './LoginPage.css'; // Importing styles for LoginPage

// PasswordResetPage component
const PasswordResetPage = () => {
  const [email, setEmail] = useState(''); // State for email
  const navigate = useNavigate(); // Hook for navigation

  const [formData, setFormData] = useState({ // State for form data
    email: '',
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
      const response = await axios.post('http://127.0.0.1:5000/resetPasswordMail', formData); // Sending POST request to reset password
      if (response.data === "success") {
        navigate('/PasswordResetCodePage'); // Navigate to PasswordResetCodePage on success
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
              <p>Please enter your email</p>
              <div className="field">
                <input className="input-field" type="email" name="email" value={formData.email} onChange={handleInputChange} placeholder="Email" required />
              </div>
              <button id="button1" className="button" type="submit" onClick={handleSubmit}>Reset</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PasswordResetPage; // Exporting PasswordResetPage component
