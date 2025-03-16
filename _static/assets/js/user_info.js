// ======================
// User Information Module
// ======================
function UserInfo() {
    this.userId = null; // Set if user is logged in
    this.deviceIp = null; // Set if user is a guest
    this.isAuthenticated = user ? true : false;
    this.wishlist = user ? user.wishlist : [];
    this.isVendor = user ? user.profile.user_type == 'vendor' : false;
    this.cartItems = user
    ? user.cart_items.map((item) => ({
        productId: item.product.id,
        productName: item.product.name, 
        weight: item.product.weight,
        width: item.product.weight, 
        height: item.product.height,
        length: item.product.length,
        quantity: item.quantity,
        price: item.product.cprice,
        color: item.color,
        size: item.size,
    }))
    : [];
  
    this.init = function () {
      // Fetch user ID if logged in (e.g., from Django template)
      this.userId = user ? user.id : null;
  
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