import React, { useEffect } from 'react'; // Importing necessary modules from React
import httpClient from './httpClient.js'; // Importing httpClient module
import { Link } from 'react-router-dom'; // Importing Link component from React Router

// SendVerification component
const SendVerification = () => {
    useEffect(() => {
        // Function to fetch verification code from server
        const fetchVerificationCode = async () => {
            try {
                const resp = await httpClient.get('http://127.0.0.1:5000/sendVerification', {
                    withCredentials: true
                });
                console.log(resp.data.code); // Log the code received from the server
            } catch (error) {
                console.log(error);
            }
        };

        fetchVerificationCode(); // Calling the function to fetch verification code
    }, []); // Running only once when the component mounts

    // Rendering JSX
    return (
        <div>
            <p>A 6 digit integer code has been printed in the terminal or sent to your email. Clicking on the button below will allow you to enter the code and get registered fully.</p>
            <Link to='/VerificationPage'>
                <button id="button" className="button" type="submit">To enter the code</button>
            </Link>
        </div>
    );
};

export default SendVerification; // Exporting SendVerification component
