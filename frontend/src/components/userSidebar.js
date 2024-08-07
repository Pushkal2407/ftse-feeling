import React from 'react'
import './userSidebar.css'


const UserDetails = () => {
  return (


    <div className="userDetailsSideBar">
        <h2>User's Name</h2>
      <ul className="button-list">
        <li><input name="email" placeholder="Email" type="email" /></li>
        <li><input name="password" placeholder="Password" type="password"/></li>
        <li><button>Show Password</button></li>
      </ul>
    </div>
  )
}

export default UserDetails