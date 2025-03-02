// ======================
// Discount Management Module
// ======================
function DiscountManager(storage, user) {
  this.storage = storage;
  this.user = user;
  const storageKey = this.user.getUserKey() + "_discounts";

  // Discount codes with applicable product IDs
  this.discountCodes = {
    "SAVE10": { 
      type: "percentage", 
      value: 10, 
      applicableProducts: [123, 456] // Applies to products with IDs 123 and 456
    },
    "FREESHIP": { 
      type: "fixed", 
      value: 500, 
      applicableProducts: [] // Applies to all products (empty array means no restriction)
    },
  };

  this.init = function () {
    if (!this.storage.getItem(storageKey)) {
      this.storage.setItem(storageKey, {}); // Initialize as an empty object
    }
  };

  // Apply a discount code to the cart
  this.applyDiscount = function (code) {
    var discount = this.discountCodes[code];
    if (!discount) {
      throw new Error("Invalid discount code");
    }

    var appliedDiscounts = this.storage.getItem(storageKey) || {};
    appliedDiscounts[code] = discount; // Store the discount code and its details
    this.storage.setItem(storageKey, appliedDiscounts);
  };

  // Remove a discount code from the cart
  this.removeDiscount = function (code) {
    var appliedDiscounts = this.storage.getItem(storageKey) || {};
    if (appliedDiscounts[code]) {
      delete appliedDiscounts[code]; // Remove the discount code
      this.storage.setItem(storageKey, appliedDiscounts);
    }
  };

  // Calculate the total discount for the cart
  this.getTotalDiscount = function (cartItems) {
    var appliedDiscounts = this.storage.getItem(storageKey) || {};
    var totalDiscount = 0;

    // Iterate over each applied discount
    Object.values(appliedDiscounts).forEach((discount) => {
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
            totalDiscount += discount.value;
          }
        }
      });
    });

    return totalDiscount;
  };
}