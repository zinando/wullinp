// callback function. if payment is successful, call verifyPayment() to verify the payment
const callback = function(response){
    triggerProcessing();
    window.location.href = '/checkout/checkout/?action=confirm-payment&txn_ref='+response.reference;
    
}

const donateCallback = function(response){
    triggerProcessing();
    window.location.href = '/checkout/checkout/?action=confirm-donation&txn_ref='+response.reference;
}

// on close callback
const onClose = function(){
    console.log('Payment closed');
    Swal.close();
}

// wishOnClose callback if first donation
const wishOnClose = function(){
    // send a request back to server to delete first order if applicable
    fetch('/user/wishlist/api/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        data: JSON.stringify({'txn_ref': metaData.custom_fields[0].txn_ref, 'action': 'delete-first-donor-order'}),
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === 1){
            // if user is registered, trigger payment
            Swal.fire('Error', `${data.message}`, 'error');
        } else {
            // if user is not registered, display an error message
            Swal.fire('Error', `${data.message}`, 'error');
        }
    });
    console.log('Payment closed');
    Swal.close();
}

// meta data for the payment
const metaData = {
    custom_fields: [
        {
            display_name: '',
            mobile_number: '',
            payment_purpose: '',
            txn_ref: '',
          },
    ]
}

// Function to verify order details before payment
function verifyOrder(order_details, onFailure){
    fetch('/checkout/checkout/?action=verify-order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify(order_details),
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === 1){
            // if order details are valid, trigger payment
            triggerPayment(data.order);
        } else {
            // if order details are invalid, display an error message
            onFailure(data.message, 'error');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        onFailure(`${error}`, 'error');
    });
}

function triggerPayment(order, type='checkout'){
    if (order.amount === 0) {
        // payment has been settled with the wallet
        console.log('Payment settled with the wallet');
        // return user to success page
        return;
    }
    metaData.custom_fields[0].display_name = order.name;
    metaData.custom_fields[0].mobile_number = order.phone;
    metaData.custom_fields[0].payment_purpose = order.paymentPurposepurpose;
    metaData.custom_fields[0].txn_ref = order.reference;
    // Initialize the payment
    const handler = PaystackPop.setup({
        key: order.paystackPublicKey,
        email: order.email,
        amount: `${order.amount * 100}`,
        ref: order.reference,
        metadata: metaData,
        callback: type === 'donation' ? donateCallback : callback,
        onClose: order.first_donor ? wishOnClose : onClose,
    });

    // Open the Paystack payment modal
    handler.openIframe();
}

// Function to donate to wishlist item
function donateToWishlistItem(userData){
    if (!userData.name || !userData.email || !userData.phone || isNaN(userData.amount)) {
        Swal.fire('Error', 'Invalid data provided.', 'error');
        return;
    }

    // Register the user in the database
    fetch('/user/wishlist/api/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify(userData),
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === 1){
            // if user is registered, trigger payment
            triggerPayment(data.order, 'donation');
        } else {
            // if user is not registered, display an error message
            Swal.fire('Error', `${data.message}`, 'error');
        }
    })
}