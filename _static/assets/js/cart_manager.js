// ======================
// Cart Management Module
// ======================
function CartManager(storage, user) {
  this.storage = storage;
  this.user = user;
  this.discountManager = new DiscountManager(storage, user);
  this.shipmentManager = new ShipmentManager(storage, user); // Add shipment manager
  const cartKey = this.user.getUserKey() + "_cart";

  this.init = function () { 
    if (!this.storage.getItem(cartKey)) {
      this.storage.setItem(cartKey, []);
    }
    this.discountManager.init();
    this.shipmentManager.init(); // Initialize shipment manager
    this.updateCartUI();
    this.updateCartCount();
  };

  this.getCart = function () {
    return this.storage.getItem(cartKey);
  };

  this.getCartTotal = function () {
    var cart = this.getCart();
    return cart.reduce((total, item) => total + item.price * item.quantity, 0);
  };

  this.addItem = function (item) {
    var cart = this.getCart();
    var existingItem = cart.find((i) => i.productId === item.productId);

    if (existingItem) {
      existingItem.quantity += item.quantity;
    } else {
      cart.push(item);
    }

    this.storage.setItem(cartKey, cart);
    this.updateCartUI();
    this.updateCartCount();

    // apply fixed dicount to each item added to cart
    this.discountManager.applyDiscount("FREESHIP");
  };

  this.removeItem = function (productId) {
    // if item quantity is more than 1, reduce quantity by 1, else remove item from cart
    var cart = this.getCart();
    var item = cart.find((i) => i.productId === productId);

    if (item.quantity > 1) {
      item.quantity -= 1;
    
    } else {
      cart = cart.filter((i) => i.productId !== productId);
    }
  
    this.storage.setItem(cartKey, cart);
    this.updateCartUI();
    this.updateCartCount();
    showToast("Item removed from cart", "info");
  };

  // add update cart count function
  this.updateCartCount = function () {
    var cart = this.getCart();
    // only count the number of items in the cart, not the quantity of each item
    var count = cart.length;
    //var count = cart.reduce((total, item) => total + item.quantity, 0);
    document.getElementById("cart-count").textContent = count;
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
    var cart = this.getCart();
    var discount = this.discountManager.getTotalDiscount(cart);
    var shippingCost = await this.getShippingCost();
    return cartTotal - discount + shippingCost;
  };

  this.updateCartUI = async function () {
    var cart = this.getCart();
    var cartTotal = this.getCartTotal();
    var discount = this.discountManager.getTotalDiscount(cart);
    var shippingCost = await this.getShippingCost();
    var discountedTotal = await this.getDiscountedTotal();

    var html = "<table class='cart-table w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400'>";
    html +="<thead class='text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400'>";
    html += "<tr>";
    html +="<th scope='col' class='px-3 py-3'>Product</th>";
    html+= "<th scope='col' class='px-3 py-3'>Price</th>";
    html += "<th scope='col' class='px-3 py-3'>Quantity</th>";
    html += "<th scope='col' class='px-3 py-3'>Total</th></tr></thead>";
    html += "<tbody>";

    cart.forEach((item) => {
      html += `<tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200">
        <td class="px-3 py-4 font-medium text-gray-800">${item.productName}</td>
        <td class="px-3 py-4">&#8358;${item.price}</td>
        <td class="px-3 py-4">${item.quantity}</td>
        <td class="px-3 py-4">&#8358;${item.price * item.quantity}</td>
        <td class="px-3 py-4"><button onclick="wullinp.cart.removeItem(${item.productId})"><i class="fas fa-trash"></i></button></td>
      </tr>`;
    });

    html += `</tbody>
      <tfoot class="border">
        <tr><td colspan="3" class="font-medium text-gray-900">Subtotal</td><td class="font-medium text-gray-900">${cartTotal}</td></tr>
        <tr><td colspan="3" class="font-medium text-gray-900">Discount</td><td class="font-medium text-gray-900">${discount}</td></tr>
        <tr><td colspan="3" class="font-medium text-gray-900">Shipping</td><td class="font-medium text-gray-900">${shippingCost}</td></tr>
        <tr><td colspan="3" class="font-medium text-gray-900">Total</td><td class="font-medium text-gray-900">${discountedTotal}</td></tr>
      </tfoot>
    </table>`;

    ///document.getElementById("cart-table").innerHTML = html;
    if (cart.length > 0) {
      document.getElementById("cart-table").innerHTML = html;
    } else {
      document.getElementById("cart-table").innerHTML = "<p class='text-center text-gray-500 dark:text-gray-400'>Your cart is empty</p>";
    }
  };
}