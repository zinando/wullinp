// ======================
// Wishlist Management Module
// ======================
function WishlistManager(storage, user) {
    this.storage = storage; 
    this.user = user;
    const storageKey = this.user.getUserKey() + "_wishlist";
  
    this.init = function () {
      if (!this.storage.getItem(storageKey)) {
        this.storage.setItem(storageKey, []);
      }
      if (!user || !user.isVendor) {
        this.updateWishlistCount();
      }
    };
  
    this.addToWishlist = function (item) {
      var wishlist = this.storage.getItem(storageKey);
      wishlist.push(item);
      this.storage.setItem(storageKey, wishlist);
    };
  
    this.removeFromWishlist = function (productId) {
      var wishlist = this.storage
        .getItem(storageKey)
        .filter((i) => i.productId !== productId);
      this.storage.setItem(storageKey, wishlist);
    };

    this.updateWishlistCount = function () {
      
      document.getElementById("wishlist-count").innerHTML = this.user.wishlist.length;
    }
  }