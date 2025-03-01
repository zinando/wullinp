// ======================
// Discount Management Module
// ======================
function DiscountManager(storage, user) {
    this.storage = storage;
    this.user = user;
  
    this.discountCodes = {
      "SAVE10": { type: "percentage", value: 10 },
      "FREESHIP": { type: "fixed", value: 500 },
    };
  
    this.init = function () {
      if (!this.storage.getItem(this.user.getUserKey() + "_discounts")) {
        this.storage.setItem(this.user.getUserKey() + "_discounts", []);
      }
    };
  
    this.applyDiscount = function (code) {
      var discount = this.discountCodes[code];
      if (!discount) {
        throw new Error("Invalid discount code");
      }
  
      var appliedDiscounts = this.storage.getItem(this.user.getUserKey() + "_discounts");
      appliedDiscounts.push(discount);
      this.storage.setItem(this.user.getUserKey() + "_discounts", appliedDiscounts);
    };
  
    this.getTotalDiscount = function (cartTotal) {
      var appliedDiscounts = this.storage.getItem(this.user.getUserKey() + "_discounts");
      return appliedDiscounts.reduce((total, discount) => {
        if (discount.type === "percentage") {
          return total + (cartTotal * discount.value) / 100;
        } else if (discount.type === "fixed") {
          return total + discount.value;
        }
        return total;
      }, 0);
    };
  }