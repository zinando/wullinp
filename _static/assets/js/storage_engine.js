// ======================
// Storage Engine Module
// ======================
function StorageEngine() {
    this.setItem = function (key, value) {
      localStorage.setItem(key, JSON.stringify(value));
    };
  
    this.getItem = function (key) {
      return JSON.parse(localStorage.getItem(key));
    };
  
    this.clear = function (key) {
      localStorage.removeItem(key);
    };
  }