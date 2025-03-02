// ======================
// User Information Module
// ======================
function UserInfo() {
    this.userId = null; // Set if user is logged in
    this.deviceIp = null; // Set if user is a guest
  
    this.init = function () {
      // Fetch user ID if logged in (e.g., from Django template)
      this.userId = window.userId || null;
  
      // Fetch device IP if user is a guest
      if (!this.userId) {
        fetch("https://api.ipify.org?format=json")
          .then((response) => response.json())
          .then((data) => {
            this.deviceIp = data.ip;
          });
      }
    }; 
  
    this.getUserKey = function () {
      return this.userId ? `user_${this.userId}` : `guest_${this.deviceIp}`;
    };
    }