// ======================
// Wallet Management Module
// ======================
function WalletManager(storage, user) {
    this.storage = storage;
    this.user = user;
    const storageKey = this.user.getUserKey() + "_wallet";
  
    this.init = function () {
      if (!this.storage.getItem(storageKey)) {
        this.storage.setItem(storageKey, { balance: 0 });
      } 
    };
  
    this.addBalance = function (amount) {
      var wallet = this.storage.getItem(storageKey);
      wallet.balance += amount;
      this.storage.setItem(storageKey, wallet);
    };
  
    this.deductBalance = function (amount) {
      var wallet = this.storage.getItem(storageKey);
      wallet.balance -= amount;
      this.storage.setItem(storageKey, wallet);
    };
  }