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
        this.states = new StatesManager(this.storage, this.site.siteProxyUrl); // Add states manager");
      
        // Initialize on creation
        this.init = function () {
            this.user.init();
            this.cart.init();
            this.wishlist.init();
            this.wallet.init();
            this.discount.init(); // Initialize discount manager
            this.shipment.init(); // Initialize shipment manager
            this.order.init();
            this.states.init();
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
    
    // create a func that takes a string and return a slug
    function slugify(string) {
        return string
            .toString()
            .normalize("NFD") // split an accented letter in the base letter and the accent
            .replace(/[\u0300-\u036f]/g, "") // remove all previously split accents
            .toLowerCase()
            .trim()
            .replace(/\s+/g, "-") // replace spaces with -
            .replace(/&/g, "-and-") // replace & with 'and'
            .replace(/[^\w-]+/g, "") // remove all non-word chars
            .replace(/--+/g, "-"); // replace multiple - with single -
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

    function triggerProcessing(){

        Swal.fire({
            title: 'Processing..',
            html: 'Confirming your transaction, please be patient',
            timerProgressBar: true,
            backdrop: true,
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });
        
    }

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

    // Function to open the product attributes modal
    function openProductAttributesModal(productId, productName, stockCount, weight, width, height, length, sizes, colors, price, type='cart') {
        // if type is wishlist, unhide the address and delivery type elements
        if(type != 'cart'){
            //console.log('wishlist');
            document.getElementById("wishAddressSelector").classList.remove("hidden");
            document.getElementById("wishDeliveryTypeSelector").classList.remove("hidden");
        } else {
            //console.log('cart');
            document.getElementById("wishAddressSelector").classList.add("hidden");
            document.getElementById("wishDeliveryTypeSelector").classList.add("hidden");
        }
        // Store product ID
        $("#confirmAddToCart").data("id", productId);
        $("#confirmAddToCart").data("name", productName);
        $("#confirmAddToCart").data("price", price);
        $("#confirmAddToCart").data("weight", weight);
        $("#confirmAddToCart").data("width", width);
        $("#confirmAddToCart").data("height", height);
        $("#confirmAddToCart").data("length", length);
        $("#confirmAddToCart").data("type", type);
    
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
            // assign it a value of null and hide the size selection
            $("#modalSize").val(null);
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
            // assign it a value of null and hide the color selection
            $("#modalColor").val(null);
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
            let weight = parseFloat($(this).data("weight"));
            let width = parseFloat($(this).data("width"));
            let height = parseFloat($(this).data("height"));
            let length = parseFloat($(this).data("length"));
            let sizes = $(this).data('sizes'); // expected to be a string array
            let colors = $(this).data("colors"); // expected to be a string array

            sizes = sizes !== null && sizes !== 'null' && sizes !== '' && sizes !== 'None' ? sizes.split(',').filter(value => value !== null && value !== undefined && value !== "") : null;
            colors = colors !== null && colors !== 'null' && colors !== '' && colors !== 'None' ? colors.split(',').filter(value => value !== null && value !== undefined && value !== "") : null;

            openProductAttributesModal(productId, productName, stockCount, weight, width, height, length, sizes, colors, price);
        });

        // Function to trigger the product attributes modal for wishlist items
        $(document).on("click", ".addToWishList", function (e) {
            e.preventDefault();
            if (!wullinp.user.isAuthenticated) {
                showToast("Please login to add items to cart", "error");
                return;
            }

            let productId = $(this).data("id");
            let productName = $(this).data("name");
            let price = parseFloat($(this).data("price"));
            let stockCount = parseInt($(this).data("stock"));
            let weight = parseFloat($(this).data("weight"));
            let width = parseFloat($(this).data("width"));
            let height = parseFloat($(this).data("height"));
            let length = parseFloat($(this).data("length"));
            let sizes = $(this).data('sizes'); // expected to be a string array
            let colors = $(this).data("colors"); // expected to be a string array

            sizes = sizes !== null && sizes !== 'null' && sizes !== '' && sizes !== 'None' ? sizes.split(',').filter(value => value !== null && value !== undefined && value !== "") : null;
            colors = colors !== null && colors !== 'null' && colors !== '' && colors !== 'None' ? colors.split(',').filter(value => value !== null && value !== undefined && value !== "") : null;

            openProductAttributesModal(productId, productName, stockCount, weight, width, height, length, sizes, colors, price, 'wishlist');
        });

        // Function to collect product attributes and add to cart
        $(document).on("click", "#confirmAddToCart", function () {

            let cart = $(this).data("type") === "cart";
            let addressId = null;
            let deliveryType = null;
            // if cart is false, check that address is selected
            if(!cart){
                // get the checked address radio button
                addressId = document.querySelector('input[name="wishAddress"]:checked');
                deliveryType = document.querySelector("input[name='deliveryType']:checked").value;
                if(!addressId){
                    showToast("Please select an address", "error");
                    return;
                }
                addressId = parseInt(addressId.value);
            }
            
            let deliveryMethod = 'home'
            let productId = $(this).data("id");
            let productName = $(this).data("name");
            let weight = parseFloat($(this).data("weight"));
            let width = parseFloat($(this).data("width"));
            let height = parseFloat($(this).data("height"));
            let length = parseFloat($(this).data("length"));
            let price = parseFloat($(this).data("price"));
            let quantity = parseInt($("#modalQuantity").val());
            let size = $("#modalSize").val() || null;
            let color = $("#modalColor").val() || null;
        
            if (quantity < 1) {
                showToast("Please enter a valid quantity", "error");
                return; 
            }
        
            let attributes = { quantity };
            attributes.size = size;
            attributes.color = color;
            
            let item = { productId, productName, price, weight, width, height, length, deliveryMethod, addressId, deliveryType, ...attributes };
            // Add item to cart or wishlist
            closeProductAttributesModal();
            if(cart){
                wullinp.cart.addItem(item);
                showToast(`${productName} added to cart`, "success");
            } else {
                addToWishlist(item);
            }
        });

        // Function to send wishlist item to backend
        function addToWishlist(item) {
            $.ajax({
                url: "/user/wishlist/api/",
                type: "POST",
                headers: { "X-CSRFToken": getCSRFToken(), "Content-Type": "application/json" },
                data: JSON.stringify(item),
                success: function (response) {
                    if (response.status === 1) {
                        document.getElementById("wishlist-count").textContent = response.count;
                        showToast(response.message, "success");
                    } else {
                        showToast(response.message, "error");
                    }   
                
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    showToast(`Error: ${errorThrown}`, "error");    
                },
            });
        }
    });

    // fetch states data from API
    wullinp.states.fetchStates();

    
    // Function to collect user data step by step
    const collectUserData = async (unpaid, wishId) => {
        let userData = {
            wishId: wishId,
            amount: null,
            name: null,
            email: null,
            phone: null,
            message: null
        };

        // Step 1: Collect Amount
        const { value: amount } = await Swal.fire({
            title: 'Contribute to Wish', //. Max: &#8358;' + unpaid,
            input: 'number',
            inputLabel: 'Amount (min: 100 - max: ' + unpaid + ')',
            inputPlaceholder: 'Enter amount',
            inputValue: userData.amount || '', // Restore previous value
            inputAttributes: {
                min: 100,
                max: unpaid
            },
            showCancelButton: true,
            confirmButtonText: 'Next',
            inputValidator: (value) => {
                if (!value) {
                    return 'Amount is required.';
                }
                if (value < 100 || value > unpaid) {
                    return `Amount must be between 100 and ${unpaid}.`;
                }
            }
        });

        if (amount) {
            userData.amount = parseFloat(amount);

            // Step 2: Collect Full Name
            const { value: name } = await Swal.fire({
                title: 'Your Full Name',
                input: 'text',
                inputLabel: 'Full Name',
                inputPlaceholder: 'Enter your full name',
                inputValue: userData.name || '', // Restore previous value
                showCancelButton: true,
                confirmButtonText: 'Next',
                inputValidator: (value) => {
                    if (!value) {
                        return 'Name is required.';
                    }
                }
            });

            if (name === null) {
                // User clicked "Back", go back to the previous step
                return collectUserData(unpaid, wishId);
            } else if (name) {
                userData.name = name;

                // Step 3: Collect Email Address
                const { value: email } = await Swal.fire({
                    title: 'Your Email Address',
                    input: 'email',
                    inputLabel: 'Email Address',
                    inputPlaceholder: 'Enter your email',
                    inputValue: userData.email || '', // Restore previous value
                    showCancelButton: true,
                    confirmButtonText: 'Next',
                    inputValidator: (value) => {
                        if (!value) {
                            return 'Email is required.';
                        }
                        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
                            return 'Valid email is required.';
                        }
                    }
                });

                if (email === null) {
                    // User clicked "Back", go back to the previous step
                    return collectUserData(unpaid, wishId);
                } else if (email) {
                    userData.email = email;

                    // Step 4: Collect Phone Number
                    const { value: phone } = await Swal.fire({
                        title: 'Your Phone Number',
                        input: 'tel',
                        inputLabel: 'Phone Number',
                        inputPlaceholder: 'Enter your phone number',
                        inputValue: userData.phone || '', // Restore previous value
                        showCancelButton: true,
                        confirmButtonText: 'Next',
                        inputValidator: (value) => {
                            if (!value) {
                                return 'Phone number is required.';
                            }
                            if (!/^\d{10,15}$/.test(value)) {
                                return 'Valid phone number is required (10-15 digits).';
                            }
                        }
                    });

                    if (phone === null) {
                        // User clicked "Back", go back to the previous step
                        return collectUserData(unpaid, wishId);
                    } else if (phone) {
                        userData.phone = phone;

                        // All steps completed, return the collected data
                        // console.log(userData);
                        // return userData;
                        // step 5: Collect Message
                        const { value: message } = await Swal.fire({
                            title: 'Add personal message to the recipient',
                            input: 'textarea',
                            inputLabel: 'This is totally optional',
                            inputPlaceholder: 'Enter your message',
                            inputValue: userData.message || '', // Restore previous value
                            showCancelButton: true,
                            confirmButtonText: 'Next',
                        });

                        // there is no back button here, so we can just get the message whether it is null or not
                        userData.message = message;
                        return userData;
                    }
                }
               

            }
        }
    };