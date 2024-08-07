import React, { useState } from 'react'; // Importing necessary modules from React
import './LoginPage.css'; // Importing styles for LoginPage component
import Parse from 'parse/dist/parse.min.js'; // Importing Parse SDK for user authentication
import { Button, Divider, Input } from 'antd'; // Importing Button, Divider, and Input components from Ant Design

// ForgotPassword component
const ForgotPassword = () => {
  const [email, setEmail] = useState(""); // State variable for storing email

  // Function to request password reset
  const doRequestPasswordReset = async () => {
    const emailValue = email; // Get email value from state
    try {
      await Parse.User.requestPasswordReset(emailValue); // Request password reset using Parse SDK
      alert(`Success! Please check ${email} to proceed with password reset.`); // Alert success message
      return true; // Return true if successful
    } catch(error) {
      alert(`Error! ${error}`); // Alert error message
      return false; // Return false if unsuccessful
    }
  };

  // Rendering JSX
  return (
    <div>
      <div className="header"> {/* Header section */}
        <img
          className="header_logo"
          alt="Back4App Logo"
          src={'https://blog.back4app.com/wp-content/uploads/2019/05/back4app-white-logo-500px.png'} // Back4App logo image
        />
        <p className="header_text_bold">{'React on Back4App'}</p> {/* Header text */}
        <p className="header_text">{'User Password Reset'}</p> {/* Header text */}
      </div>
      <div className="container"> {/* Main container */}
        <h2 className="heading">{'Request password reset email'}</h2> {/* Heading */}
        <Divider /> {/* Divider */}
        <div className="form_wrapper"> {/* Form wrapper */}
          <Input
            value={email}
            onChange={(event) => setEmail(event.target.value)} // Update email state on change
            placeholder="Your account email"
            size="large"
            className="form_input"
          />
        </div>
        <div className="form_buttons"> {/* Form buttons */}
          <Button
            onClick={doRequestPasswordReset} // Call doRequestPasswordReset function on button click
            type="primary"
            className="form_button"
            color={'#208AEC'}
            size="large"
          >
            Request password reset
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword; // Exporting ForgotPassword component
