// ======================
// States Data Management Module
// ======================
function StatesManager(storage, apiUrl) {
    this.storage = storage;
    this.apiUrl = apiUrl;
    const storageKey = "states_data";
    const lastFetchKey = "states_last_fetch";
  
    // Initialize states data
    this.init = function () {
      if (!this.storage.getItem(storageKey)) {
        this.storage.setItem(storageKey, []); // Initialize as empty array
      }
    };
  
    // Fetch states data from API if outdated or not available
    this.fetchStates = async function () {
      const lastFetch = this.storage.getItem(lastFetchKey);
      const now = new Date().getTime();
      const oneDay = 24 * 60 * 60 * 1000; // One day in milliseconds
  
      // Only fetch if more than 24 hours have passed
      if (!lastFetch || now - lastFetch > oneDay) {
        try {
          const response = await fetch(this.apiUrl);
          if (!response.ok) throw new Error("Failed to fetch states data");
          
          const statesData = await response.json();
          this.storage.setItem(storageKey, statesData.data); // Store states data as an array
          this.storage.setItem(lastFetchKey, now); // Update last fetch timestamp
          console.log("States data updated.");
        } catch (error) {
          console.error("Error fetching states data:", error);
        }
      } else {
        console.log("Using cached states data.");
      }
    };
  
    // Get all states
    this.getStates = function () {
      return this.storage.getItem(storageKey) || [];
    };
  
    // Find a state by ID
    this.getStateById = function (stateId) {
      const states = this.getStates();
      return states.find((state) => state.id === stateId) || null;
    };
  
    // Find a state by name
    this.getStateByName = function (stateName) {
      const states = this.getStates();
      return states.find((state) => state.name.toLowerCase() === stateName.toLowerCase()) || null;
    };
  }
  
//   // ======================
//   // Usage Example
//   // ======================
//   const statesManager = new StatesManager(localStorage, "https://gps-naija.onrender.com/states");
  
//   statesManager.init();
//   statesManager.fetchStates(); // Fetch data if needed
  
//   // Example usage after fetching
//   setTimeout(() => {
//     console.log("All States:", statesManager.getStates());
//     console.log("Find State by ID (1):", statesManager.getStateById(1));
//     console.log("Find State by Name (Lagos):", statesManager.getStateByName("Lagos"));
//   }, 2000);
  