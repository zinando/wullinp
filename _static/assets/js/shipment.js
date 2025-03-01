// ======================
// Shipment Management Module
// ======================
function ShipmentManager(storage, user) {
    this.storage = storage;
    this.user = user;
  
    // Constants
    this.freeShippingThreshold = 20000; // Free shipping for orders above ₦20,000
    this.volumetricDivisor = 5000; // Used for volumetric weight calculation
    this.perKgRate = 200; // Default per kg rate if external API fails
    this.baseCost = 1000; // Base shipping cost
  
    // Initialize
    this.init = function () {
      if (!this.storage.getItem(this.user.getUserKey() + "_shipping")) {
        this.storage.setItem(this.user.getUserKey() + "_shipping", {
          city: null,
          deliveryMethod: "standard",
          preferredCourier: "GIG", // Default to GIG Logistics
        });
      }
    };
  
    // Set shipping information
    this.setShippingInfo = function (city, deliveryMethod, preferredCourier) {
      var shippingInfo = this.storage.getItem(this.user.getUserKey() + "_shipping");
      shippingInfo.city = city;
      shippingInfo.deliveryMethod = deliveryMethod;
      shippingInfo.preferredCourier = preferredCourier || "GIG";
      this.storage.setItem(this.user.getUserKey() + "_shipping", shippingInfo);
    };
  
    // Fetch courier rates from an external API
    this.getCourierRates = async function (city, deliveryMethod) {
      try {
        const response = await axios.get("https://api.example.com/shipping-rates", {
          params: { city, deliveryMethod },
        });
  
        if (response.data && response.data.rates) {
          return response.data.rates; // Assume API returns { "DHL": 1.2, "FedEx": 1.5, "GIG": 1.0 }
        }
      } catch (error) {
        console.error("Failed to fetch courier rates:", error);
      }
  
      // Fallback rates if API request fails
      return { DHL: 1.2, FedEx: 1.5, GIG: 1.0 };
    };
  
    // Calculate shipping cost dynamically
    this.calculateShippingCost = async function (order) {
      var shippingInfo = this.storage.getItem(this.user.getUserKey() + "_shipping");
      var city = shippingInfo.city || "Remote Area";
      var deliveryMethod = shippingInfo.deliveryMethod || "standard";
      var preferredCourier = shippingInfo.preferredCourier || "GIG";
      var isJumiaExpress = order.isJumiaExpress || false;
  
      // Fetch courier rates
      var courierRates = await this.getCourierRates(city, deliveryMethod);
      var shippingMultiplier = courierRates[preferredCourier] || 1.0;
  
      // Calculate total weight and special handling fees
      var totalWeight = 0;
      var specialHandlingFee = 0;
  
      order.items.forEach((item) => {
        var weight = item.weight || 1;
        var volumetricWeight = (item.length * item.width * item.height) / this.volumetricDivisor;
        var effectiveWeight = Math.max(weight, volumetricWeight);
  
        totalWeight += effectiveWeight;
  
        if (item.isFragile) specialHandlingFee += 500;
        if (item.isBulky) specialHandlingFee += 1000;
      });
  
      // Calculate shipping cost
      var weightCharge = totalWeight * this.perKgRate;
      var baseCost = this.baseCost * shippingMultiplier;
      var shippingCost = baseCost + weightCharge + specialHandlingFee;
  
      // Free shipping for high-value orders
      if (order.totalAmount >= this.freeShippingThreshold) shippingCost = 0;
  
      // Discount for Jumia Express
      if (isJumiaExpress) shippingCost *= 0.8;
  
      return Math.ceil(shippingCost);
    };
  }