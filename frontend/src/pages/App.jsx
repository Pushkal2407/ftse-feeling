import { GoogleLogin, useGoogleLogin } from '@react-oauth/google'; // Importing Google OAuth components and hooks
import { GoogleOAuthProvider } from '@react-oauth/google'; // Importing Google OAuth provider
import { jwtDecode } from "jwt-decode"; // Importing jwtDecode function to decode credentials
import { UseGoogleLogin } from '@react-oauth/google'; // Importing incorrect module, unnecessary
import axios from "axios"; // Importing axios for making HTTP requests
import {
    createBrowserRouter, // Importing createBrowserRouter for routing, but not used in the code
    RouterProvider,
    useNavigate // Importing useNavigate for routing, but not used in the code
} from "react-router-dom"; // Importing React Router components for routing, but not used in the code

function App() {
    const login = useGoogleLogin({ // Using useGoogleLogin hook to handle Google OAuth login
        onSuccess: async (response) => { // Callback function executed on successful login
            try {
                const res = await axios.get( // Making GET request to Google userinfo endpoint
                    "https://www.googleapis.com/oauth2/v3/userinfo",
                    {
                        headers: {
                            Authorization: `Bearer ${response.accessToken}` // Setting Authorization header with access token
                        }
                    }
                );                
                console.log(res); // Logging the response from userinfo endpoint
            } catch (err) {
                console.log(err); // Logging any errors that occur during the request
            }
        }
    });
    return (
        <GoogleLogin // GoogleLogin component for rendering Google OAuth login button
            onSuccess={credentialResponse => { // Callback function executed on successful login
                const credentialResponseDecoded = jwtDecode(credentialResponse.credential); // Decoding the credential response
                console.log(credentialResponseDecoded); // Logging the decoded credential response
            }}
            onError={() => { // Callback function executed on login error
                console.log('Login Failed'); // Logging login failure
            }}
        />
    );
}
