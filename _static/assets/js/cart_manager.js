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
    this.initCart();

    this.discountManager.init();
    this.shipmentManager.init(); // Initialize shipment manager
    if (!user || !user.isVendor) {
      this.updateCartUI();
      this.updateCartCount();
    }
  };

  this.initCart = function () {
    if (this.user.isAuthenticated) {
        this.user.cartItems.forEach((item) => {
            if (!this.getCart().some(cartItem => cartItem.productId === item.productId && cartItem.color === item.color && cartItem.size === item.size)) {
              // also check for color and size
               
                this.addItem(item);
            }
        });
    }
};

  this.getCart = function () {
    return this.storage.getItem(cartKey);
  };

  // function to get a single item from cart
  this.getItem = function (productId) {
    var cart = this.getCart();
    return cart.find((i) => i.productId === productId);
  };

  this.getCartTotal = function () {
    var cart = this.getCart();
    return cart.reduce((total, item) => total + item.price * item.quantity, 0);
  };

  this.addItem = function (item) {
      var cart = this.getCart();

      // Find all items with the same productId
      var matchingItems = cart.filter((i) => i.productId === item.productId);

      // Check if any of the matching items have the same color and size
      var existingItem = matchingItems.find((i) => 
          i.color === item.color && i.size === item.size
      );

      if (existingItem) {
          existingItem.quantity += item.quantity;
      } else {
          cart.push(item);
      }

      this.storage.setItem(cartKey, cart);
      this.updateCartUI();
      this.updateCartCount();

      // update the database cart if user is logged in
      if (this.user.isAuthenticated) {
        this.updateDatabaseCart();
      }
  };


  // method to update cart item quantity
  this.updateItem = function (productId, quantity) {
    var cart = this.getCart();
    var item = cart.find((i) => i.productId === productId);
    item.quantity = quantity;
    this.storage.setItem(cartKey, cart);
    this.updateCartUI();
    this.updateCartCount();
  };

  this.removeItem = function (productId, color, size) {
      var cart = this.getCart();
      color = color === "None" || color === null || color === '' || color === 'null' ? null : color;
      size = size === "None" || size === null || size === '' || size === 'null' ? null : size;

      console.log(`Removing item with productId: ${productId}, color: ${color}, size: ${size}`);

      // Find the item with the same productId, color, and size
      var itemIndex = cart.findIndex((i) => 
          i.productId === productId && i.color === color && i.size === size
      );

      console.log(`item index: ${itemIndex}`);

      if (itemIndex !== -1) {
        cart.splice(itemIndex, 1); // Remove the item from the cart
      }

      this.storage.setItem(cartKey, cart);
      this.updateCartUI();
      this.updateCartCount();
      showToast("Item removed from cart", "info");

      // update the database cart if user is logged in
      if (this.user.isAuthenticated) {
        this.updateDatabaseCart();
      }
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
    return await this.shipmentManager.calculateShippingCost(cart);
  };

  this.getDiscount = async function () {
    var cart = this.getCart();
    return await this.discountManager.getTotalDiscount(cart);
  }

  this.getDiscountedTotal = async function () {
    var cartTotal = this.getCartTotal();
    var discount = await this.getDiscount();
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
        <td class="px-3 py-4"><button onclick="wullinp.cart.removeItem(${item.productId}, '${item.color}', '${item.size}')"><i class="fas fa-trash"></i></button></td>
      </tr>`;
    });

    html += `</tbody>
      <tfoot class="border">
        <tr><td colspan="3" class="font-medium text-gray-900">Subtotal</td><td class="font-medium text-gray-900">${cartTotal}</td></tr>
        <tr><td colspan="3" class="font-medium text-gray-900">Discount</td><td class="font-medium text-gray-900">${discount}</td></tr>
        <tr><td colspan="3" class="font-medium text-gray-900">Shipping (estimated)</td><td class="font-medium text-gray-900">${shippingCost}</td></tr>
        <tr><td colspan="3" class="font-medium text-gray-900">Total (estimated)</td><td class="font-medium text-gray-900">${discountedTotal}</td></tr>
      </tfoot>
    </table>`;

    ///document.getElementById("cart-table").innerHTML = html;
    if (cart.length > 0) {
      document.getElementById("cart-table").innerHTML = html;
    } else {
      document.getElementById("cart-table").innerHTML = "<p class='text-center text-gray-500 dark:text-gray-400'>Your cart is empty</p>";
    }
  };

  this.clearCart = function () {
    this.storage.setItem(cartKey, []);
    this.updateCartUI();
    this.updateCartCount();

    // update the database cart if user is logged in
    if (this.user.isAuthenticated) {
      this.updateDatabaseCart();
    }
  };

  this.updateDatabaseCart = async function () {
      try {
        // Prepare request payload
        const cartItems = this.getCart();
        const response = await fetch("/checkout/checkout/?action=save-cart", {
            method: "POST",
            body: JSON.stringify(cartItems),
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            }
        });

        // Check if request was successful
        if (!response.ok) {
            return false;
        }
        return true;
    } catch (error) {
        console.error("Error during checkout:", error);
        showToast("An error occurred during checkout. Please try again.", "error");
        return false;
    }
  };
}