// ======================
// Shipment Management Module
// ======================
function ShipmentManager(storage, user) {
  this.storage = storage;
  this.user = user;
  const storageKey = this.user.getUserKey() + "_shipping";

  // Constants
  this.baseCost = 2000; // Base shipping cost per order
  this.weightFactor = 100; // Cost per kg
  this.internationalSurcharge = 2000; // Additional cost for international shipping
  this.nonLagosSurcharge = 1000; // Additional cost for non-Lagos addresses
  this.expressDeliverySurcharge = 1000; // Additional cost for express delivery
  this.homeDeliverySurcharge = 1000; // Additional cost for home delivery

  // Initialize
  this.init = function () {
    if (!this.storage.getItem(storageKey)) {
      this.storage.setItem(storageKey, {
        id: 0,
        city: "",
        state: "",
        country: "Nigeria",
        deliveryMethod: "home",
        deliveryType: "regular",
      });
    }
  };

  this.getShippingInfo = function () {
    return this.storage.getItem(storageKey);
  };

  // Set shipping information
  this.setShippingInfo = function (key, value) {
    var shippingInfo = this.storage.getItem(storageKey);
    shippingInfo[key] = value;
    this.storage.setItem(storageKey, shippingInfo);
  };

  // Calculate shipping cost dynamically
  this.calculateShippingCost = function (cartItems) {
    // Calculate total weight of the order
    var totalWeight = 0;
    cartItems.forEach((item) => {
      totalWeight += item.weight * item.quantity;
    });

    // Initialize shipping cost with base cost
    var shippingCost = this.baseCost;

    // Apply surcharges based on user address
    var shippingInfo = this.storage.getItem(storageKey);
    if (shippingInfo.country.toLowerCase() !== "nigeria") {
      shippingCost += this.internationalSurcharge;
    } else if (shippingInfo.state.toLowerCase() !== "lagos") {
      shippingCost += this.nonLagosSurcharge;
    }

    // Apply surcharges based on delivery type and method
    if (shippingInfo.deliveryType === "express") {
      shippingCost += this.expressDeliverySurcharge;
    }

    if (shippingInfo.deliveryMethod === "home") {
      shippingCost += this.homeDeliverySurcharge;
    }

    // Add weight-based cost
    shippingCost += totalWeight * this.weightFactor;

    return shippingCost;
  };
}