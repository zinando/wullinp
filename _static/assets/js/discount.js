// ======================
// Discount Management Module
// ======================
function DiscountManager(storage, user) {
  this.storage = storage;
  this.user = user;
  const storageKey = this.user.getUserKey() + "_discounts";

  // Discount codes with applicable product IDs
  this.discountCode = function () {
    return this.storage.getItem(storageKey) || {};
  }

  this.init = function () {
    if (!this.storage.getItem(storageKey)) {
      this.storage.setItem(storageKey, {}); // Initialize as an empty object
    }
  };

  // Apply a discount code to the cart
  this.applyDiscount = function (code) {
    var appliedDiscount = this.storage.getItem(storageKey) || {};
    appliedDiscount = code; // Store the discount code and its details
    this.storage.setItem(storageKey, appliedDiscount);
  };

  // Remove a discount code from the cart
  this.removeDiscount = function () {
    this.storage.setItem(storageKey, {});
  };

  // Calculate the total discount for the cart
  this.getTotalDiscount = function (cartItems) {
    var discount = this.discountCode();
    var totalDiscount = 0;

    // if discount is not set or is empty, return 0
    if (!discount || Object.keys(discount).length === 0) {
      return 0;
    }

    // check if minprice is met
    if (discount.minPurchase && discount.minPurchase > cartItems.reduce((acc, item) => acc + item.price * item.quantity, 0)) {
      return 0;
    }
      // Iterate over each product in the cart
      cartItems.forEach((item) => {
        // Check if the discount applies to the product
        if (
          discount.applicableProducts.length === 0 || // No restriction (applies to all products)
          discount.applicableProducts.includes(item.productId) // Applies to specific products
        ) {
          if (discount.type === "percentage") {
            totalDiscount += (item.price * item.quantity * discount.value) / 100;
          } else if (discount.type === "fixed") {
            totalDiscount += discount.value * item.quantity;
          }
        }
      });

    return totalDiscount;
  };
}