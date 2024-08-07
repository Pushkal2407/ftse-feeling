import React, { useState } from 'react'; // Importing necessary modules from React
import { useNavigate } from "react-router-dom"; // Importing useNavigate hook from React Router
import axios from "axios"; // Importing axios for HTTP requests
import logo from '../assets/ftse-logo.png'; // Importing logo image
import Alert from '@mui/material/Alert'; // Importing Alert component from Material-UI
import Stack from '@mui/material/Stack'; // Importing Stack component from Material-UI
import './LoginPage.css'; // Importing styles for LoginPage

// Verification component
const Verification = () => {
    const [code, setCode] = useState(''); // State for verification code
    const navigate = useNavigate(); // Hook for navigation
    const [errorMessage, setErrorMessage] = useState(''); // State for error message

    const [formData, setFormData] = useState({ // State for form data
        code: ''
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
            const resp = await axios.post('http://127.0.0.1:5000/checkRegistrationCode', formData); // Sending POST request to check verification code
            console.log(resp.data);
            if (resp.data === "success") {
                navigate('/Login'); // Navigate to Login page on success
            } else {
                setErrorMessage(resp.data); // Set error message if verification fails
            }
        } catch (error) {
            console.log(error);
        }
    };

    // Rendering JSX
    return (
        <div className='LoginPage'>
            <img src={logo} alt="Logo" className='logo' />
            <div className='card-container'>
                <div className='card'>
                    <div className="card2">
                        <form className="form" onSubmit={handleSubmit}>
                            <p className="heading">Verification</p>
                            <div className="field">
                                <input className="input-field" type="number" name="code" value={formData.email} onChange={handleInputChange} placeholder="xxxxxx" minLength="6" maxLength="6" required />
                            </div>
                            <button id="button1" className="button" type="submit" onClick={handleSubmit}>Submit</button>
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

export default Verification; // Exporting Verification component
