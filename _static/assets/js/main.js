    // ======================
    // Wullinp Core Function
    // ======================
    function Wullinp() {
        var self = this;

        //localStorage.clear(); // Clear local storage on page load
      
        // Initialize modules
        this.storage = new StorageEngine();
        this.site = new SiteInfo();
        this.user = new UserInfo();
        this.cart = new CartManager(this.storage, this.user);
        this.order = new OrderManager(this.storage, this.user);
        this.wishlist = new WishlistManager(this.storage, this.user);
        this.wallet = new WalletManager(this.storage, this.user);
        this.discount = new DiscountManager(this.storage, this.user); // Add discount manager
        this.shipment = new ShipmentManager(this.storage, this.user); // Add shipment manager
      
        // Initialize on creation
        this.init = function () {
            this.user.init();
            this.cart.init();
            this.wishlist.init();
            this.wallet.init();
            this.discount.init(); // Initialize discount manager
            this.shipment.init(); // Initialize shipment manager
            this.order.init();
        };
      
        this.init();
      }

    // ======================
    // Initialize Wullinp
    // ======================
    var wullinp = new Wullinp();

    // Function to get CSRF token from cookies
    function getCSRFToken() {
        const name = "csrftoken";
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // function to show loading spinner
    function showLoading(selector) {
        selector.innerHTML =
    '<svg class="animate-spin h-5 w-5 mr-2 text-white" viewBox="0 0 24 24"> <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle> <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 0116 0"></path> </svg> sending request...';
        selector.disabled = true;
    }

    // function to hide loading spinner
    function hideLoading(selector, text) {
        selector.innerHTML = text;
        selector.disabled = false;
    }

    // function to disable clicks on any button
    function disableButton(button) {
        button.classList.add("disabled-link");  // Add class to disable hover effect
        button.style.pointerEvents = "none";  // Disable clicks
        button.style.opacity = "0.5";  // Reduce visibility
    }

    // function to enable clicks on any button
    function enableButton(button) {
        button.classList.remove("disabled-link");  // Remove class to enable hover effect
        button.style.pointerEvents = "auto";  // Enable clicks
        button.style.opacity = "1";  // Restore visibility
    }

    // // function to show a toast message
    // function showToast(message, type) {
    //     const toast = document.getElementById("toast");
    //     toast.classList.add("show-toast");
    //     toast.classList.add(type);
    //     toast.innerText = message;
    //     setTimeout(() => {
    //         toast.classList.remove("show-toast");
    //         toast.classList.remove(type);
    //     }, 5000);
    // }

    // for managing data that should persist across page reloads
    class LocalStorageManager {
        constructor(storageKey) {
            this.storageKey = storageKey;
        }

        // Save data to localStorage
        saveData(data) {
            localStorage.setItem(this.storageKey, JSON.stringify(data));
        }

        // Retrieve data from localStorage
        getData() {
            return JSON.parse(localStorage.getItem(this.storageKey)) || [];
        }

        // Add a new item to stored data
        addItem(item) {
            let data = this.getData();
            data.push(item);
            this.saveData(data);
        }

        // Update an item in the stored data (based on an ID or key)
        updateItem(id, updatedItem) {
            let data = this.getData();
            data = data.map(item => item.id === id ? { ...item, ...updatedItem } : item);
            this.saveData(data);
        }

        // Remove an item from stored data by ID
        removeItem(id) {
            let data = this.getData().filter(item => item.id !== id);
            this.saveData(data);
        }

        // Clear all stored data
        clearData() {
            localStorage.removeItem(this.storageKey);
        }
    }

    // initialize the local storage manager
    const displayProducts = new LocalStorageManager('displayProducts');

    // function to show toast
    function showToast(message, type) {
        let toast = document.getElementById("toast");
        let toastColors = {
            success: "bg-green-500",
            error: "bg-red-500",
            warning: "bg-yellow-500",
            info: "bg-blue-500",
        };
        
        toast.textContent = message;
        toast.className = `fixed top-5 right-5 px-4 py-2 rounded shadow-lg text-white ${toastColors[type]} opacity-100`;
        toast.classList.remove("hidden");
        
        setTimeout(() => {
            toast.classList.add("opacity-0");
            setTimeout(() => toast.classList.add("hidden"), 500);
        }, 3000);
    }

    // class Cart {
    //     constructor() {
    //         this.cart = JSON.parse(localStorage.getItem("cart")) || {};
    //         this.updateCartCount();
    //     }
    
    //     addToCart(productId, productName, attributes) {
    //         if (this.cart[productId]) {
    //             this.cart[productId].quantity += attributes.quantity;
    //         } else {
    //             this.cart[productId] = { name: productName, ...attributes };
    //         }
    //         this.saveCart();
    //         showToast(`${productName} added to cart`, "success");
    //     }
    
    //     saveCart() {
    //         localStorage.setItem("cart", JSON.stringify(this.cart));
    //         this.updateCartCount();
    //     }
    
    //     updateCartCount() {
    //         let count = Object.keys(this.cart).length;
    //         document.getElementById("cart-count").textContent = count;
    //     }
    // }

    // const cart = new Cart();

    // Function to open the product attributes modal
    function openProductAttributesModal(productId, productName, stockCount, sizes, colors, price) {
        // Store product ID
        $("#confirmAddToCart").data("id", productId);
        $("#confirmAddToCart").data("name", productName);
        $("#confirmAddToCart").data("price", price);
    
        // Set Modal Title
        $("#modalTitle").text(`Select Options for ${productName}`);
    
        // Set Quantity Field (Limit to Stock Count)
        $("#modalQuantity").attr("max", stockCount).val(1);
    
        // Populate Sizes Dropdown (If Available)
        if (sizes && sizes.length > 0) {
            $("#sizeSelection").removeClass("hidden");
            let sizeDropdown = $("#modalSize").empty();
            sizes.forEach(size => {
                sizeDropdown.append(`<option value="${size}">${size}</option>`);
            });
        } else {
            $("#sizeSelection").addClass("hidden");
        }
    
        // Populate Colors Dropdown (If Available)
        if (colors && colors.length > 0) {
            $("#colorSelection").removeClass("hidden");
            let colorDropdown = $("#modalColor").empty();
            colors.forEach(color => {
                colorDropdown.append(`<option value="${color}">${color}</option>`);
            });
        } else {
            $("#colorSelection").addClass("hidden");
        }
    
        // Show Modal
        $("#productModal").removeClass("hidden");
    }

    // Function to close the product attributes modal
    function closeProductAttributesModal() {
        $("#productModal").addClass("hidden");
    }
    
    $(document).ready(function() {
       // Function to trigger the product attributes modal
        $(document).on("click", ".addToCart", function () {
            let productId = $(this).data("id");
            let productName = $(this).data("name");
            let price = parseFloat($(this).data("price"));
            let stockCount = parseInt($(this).data("stock"));
            let sizes = "[24, 26, 28, 30, 32]"; //$(this).data("sizes"); // Expected to be an array
            let colors = '["red", "blue", "green", "black", "silver"]'; //$(this).data("colors"); // Expected to be an array

            // if sizes and colors are strings, convert them to arrays
            sizes = JSON.parse(sizes || "[]");
            colors = JSON.parse(colors || "[]");

            openProductAttributesModal(productId, productName, stockCount, sizes, colors, price);
        });

        // Function to collect product attributes and add to cart
        $(document).on("click", "#confirmAddToCart", function () {
            let productId = $(this).data("id");
            let productName = $(this).data("name");
            let price = parseFloat($(this).data("price"));
            let quantity = parseInt($("#modalQuantity").val());
            let size = $("#modalSize").val() || null;
            let color = $("#modalColor").val() || null;
        
            if (quantity < 1) {
                showToast("Please enter a valid quantity", "error");
                return;
            }
        
            let attributes = { quantity };
            if (size) attributes.size = size;
            if (color) attributes.color = color;
        
            //cart.addToCart(productId, productName, attributes);
            wullinp.cart.addItem({ productId, productName, price, ...attributes });
            closeProductAttributesModal();
            showToast(`${productName} added to cart`, "success");
        });
    });
    

