// ======================
// Wishlist Management Module
// ======================
function WishlistManager(storage, user) {
    this.storage = storage;
    this.user = user;
  
    this.init = function () {
      if (!this.storage.getItem(this.user.getUserKey() + "_wishlist")) {
        this.storage.setItem(this.user.getUserKey() + "_wishlist", []);
      }
    };
  
    this.addToWishlist = function (item) {
      var wishlist = this.storage.getItem(this.user.getUserKey() + "_wishlist");
      wishlist.push(item);
      this.storage.setItem(this.user.getUserKey() + "_wishlist", wishlist);
    };
  
    this.removeFromWishlist = function (productId) {
      var wishlist = this.storage
        .getItem(this.user.getUserKey() + "_wishlist")
        .filter((i) => i.productId !== productId);
      this.storage.setItem(this.user.getUserKey() + "_wishlist", wishlist);
    };
  }