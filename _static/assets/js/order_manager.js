// ======================
// Order Management Module
// ======================
function OrderManager(storage, user) {
  this.storage = storage;
  this.user = user;
  this.cartManager = new CartManager(storage, user);
  const orderKey = this.user.getUserKey() + "_orders";

  this.init = function () {
    if (!this.storage.getItem(orderKey)) {
      this.storage.setItem(orderKey, []);
    }
  }

  this.placeOrder = async function (paymentGateway) {
    var cart = this.storage.getItem(orderKey);

    if (cart.length === 0) {
      alert("Your cart is empty!");
      return;
    }
 
    var order = {
      userId: this.user.userId,
      deviceIp: this.user.deviceIp,
      items: cart,
      paymentGateway: paymentGateway,
      subtotal: this.cartManager.getCartTotal(),
      discount: this.cartManager.discountManager.getTotalDiscount(this.cartManager.getCartTotal()),
      shippingCost: await this.cartManager.getShippingCost(),
      total: await this.cartManager.getDiscountedTotal(),
    };

    // Simulate order placement (replace with actual API call)
    console.log("Order placed:", order);
    this.storage.setItem(orderKey, order);
    this.clearCart();
  };
}