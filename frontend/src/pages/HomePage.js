import React from 'react'
import Navbar from '../components/NavBar/navbar'
import SuggestedCompanies from '../components/SuggestedCompanies'
import './HomePage.css'
import FollowedCompanies from '../components/FollowedCompanies'
import NewsButton from '../components/NewsButton'

// main function
const HomePage = () => {

  return (

    <div className='page'>
        <Navbar></Navbar>

        <SuggestedCompanies className='suggested'></SuggestedCompanies>
        <FollowedCompanies className='followed'></FollowedCompanies>
        <NewsButton className='Nbuttons'></NewsButton>
    </div>
  )
}

export default HomePage