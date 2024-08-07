import React, { useState, useCallback, useEffect } from 'react';
 import Navbar from '../components/NavBar/navbar'
import ProfileSidebar from '../components/ProfileSidebar'
import ProfileBox from '../components/ProfileBox'
import './ProfilePage.css'

// Main function
const ProfilePage = () => {
  return (
    <div className='ProfilePage'>
      <Navbar></Navbar> 
      <ProfileBox className='Pbuttons'></ProfileBox>
      <ProfileSidebar className='ProfileSidebar'></ProfileSidebar>

    </div>
  )
}

export default ProfilePage
