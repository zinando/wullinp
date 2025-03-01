// ======================
// Order Management Module
// ======================
function OrderManager(storage, user) {
  this.storage = storage;
  this.user = user;
  this.cartManager = new CartManager(storage, user);

  this.placeOrder = async function (paymentGateway) {
    var cart = this.storage.getItem(this.user.getUserKey() + "_cart");

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
    this.storage.setItem(this.user.getUserKey() + "_orders", order);
    this.clearCart();
  };
}