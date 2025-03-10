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

    this.getBalance = async function () {
        // return this.storage.getItem(storageKey).balance;
        var response = await fetch('/user/wallet/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
        });
        if (response.ok) {
            var data = await response.json();
            return data.balance;
        } else {
            console.error('Error:', response.statusText);
            return 0;
        }
    };
}