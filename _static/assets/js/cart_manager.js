// ======================
// Cart Management Module
// ======================
function CartManager(storage, user) {
  this.storage = storage;
  this.user = user;
  this.discountManager = new DiscountManager(storage, user);
  this.shipmentManager = new ShipmentManager(storage, user); // Add shipment manager

  this.init = function () {
    if (!this.storage.getItem(this.user.getUserKey() + "_cart")) {
      this.storage.setItem(this.user.getUserKey() + "_cart", []);
    }
    this.discountManager.init();
    this.shipmentManager.init(); // Initialize shipment manager
  };

  this.getCartTotal = function () {
    var cart = this.getCart();
    return cart.reduce((total, item) => total + item.price * item.quantity, 0);
  };

  this.getShippingCost = async function () {
    var cart = this.getCart();
    var order = {
      items: cart,
      totalAmount: this.getCartTotal(),
      isJumiaExpress: false, // Set based on order fulfillment method
    };
    return await this.shipmentManager.calculateShippingCost(order);
  };

  this.getDiscountedTotal = async function () {
    var cartTotal = this.getCartTotal();
    var discount = this.discountManager.getTotalDiscount(cartTotal);
    var shippingCost = await this.getShippingCost();
    return cartTotal - discount + shippingCost;
  };

  this.updateCartUI = async function () {
    var cart = this.getCart();
    var cartTotal = this.getCartTotal();
    var discount = this.discountManager.getTotalDiscount(cartTotal);
    var shippingCost = await this.getShippingCost();
    var discountedTotal = await this.getDiscountedTotal();

    var html = "<table class='cart-table'><thead><tr><th>Product</th><th>Price</th><th>Quantity</th><th>Total</th></tr></thead><tbody>";

    cart.forEach((item) => {
      html += `<tr>
        <td>${item.productName}</td>
        <td>${item.price}</td>
        <td>${item.quantity}</td>
        <td>${item.price * item.quantity}</td>
      </tr>`;
    });

    html += `</tbody>
      <tfoot>
        <tr><td colspan="3">Subtotal</td><td>${cartTotal}</td></tr>
        <tr><td colspan="3">Discount</td><td>${discount}</td></tr>
        <tr><td colspan="3">Shipping</td><td>${shippingCost}</td></tr>
        <tr><td colspan="3">Total</td><td>${discountedTotal}</td></tr>
      </tfoot>
    </table>`;

    document.getElementById("cart-table").innerHTML = html;
  };
}