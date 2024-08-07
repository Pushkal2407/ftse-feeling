import React, { useState, useEffect} from 'react';
import './UnfollowButton.css'
import axios from "axios";

function MyTick() {
    const queryParams = new URLSearchParams(window.location.search); // Creating a new URLSearchParams object with the current URL's query string
    const value = queryParams.get('name'); // Retrieve the value of a specific query parameter
    return value;
}

function UnfollowButton(){

    const data = {
        ticker: MyTick(),
      };

    const follow = async (event) => {
        event.preventDefault();
    
        try {
          const response = await axios.post('http://127.0.0.1:5000/removeFollow', data); // Sending POST request to unfollow 
        } catch (error) {
          console.error('unfollow failed', error.message);
        }
      };
    return(
        
<button type="UFbutton" class="UFbutton" onClick={follow}>
  <span class="UFbutton__text">Unfollow</span>
  <span class="UFbutton__icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" viewBox="0 0 24 24" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" stroke="currentColor" height="24" fill="none" class="svg"><line y2="19" y1="5" x2="12" x1="12"></line><line y2="12" y1="12" x2="19" x1="5"></line></svg></span>
</button>
    );
}

export default UnfollowButton
