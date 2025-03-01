// ======================
// Wallet Management Module
// ======================
function WalletManager(storage, user) {
    this.storage = storage;
    this.user = user;
  
    this.init = function () {
      if (!this.storage.getItem(this.user.getUserKey() + "_wallet")) {
        this.storage.setItem(this.user.getUserKey() + "_wallet", { balance: 0 });
      }
    };
  
    this.addBalance = function (amount) {
      var wallet = this.storage.getItem(this.user.getUserKey() + "_wallet");
      wallet.balance += amount;
      this.storage.setItem(this.user.getUserKey() + "_wallet", wallet);
    };
  
    this.deductBalance = function (amount) {
      var wallet = this.storage.getItem(this.user.getUserKey() + "_wallet");
      wallet.balance -= amount;
      this.storage.setItem(this.user.getUserKey() + "_wallet", wallet);
    };
  }