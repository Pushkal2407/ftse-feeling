import React, { Component } from "react";

class DesktopNotification extends Component {
  constructor() {
    super();
    this.showNotification = this.showNotification.bind(this);
  }

  componentDidMount() {
    if (!("Notification" in window)) {
      console.log("Browser does not support desktop notification");
    } else {
      Notification.requestPermission(); // Requesting permission for desktop notifications if supported
    }
  }

  // Function to show desktop notification
  showNotification() {
    new Notification('There has been a development in a company that you follow')
  }

  render() {
    return (<div></div>
    );
  }
}

export default DesktopNotification;