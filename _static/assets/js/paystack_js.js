// callback function. if payment is successful, call verifyPayment() to verify the payment
const callback = function(response){
    triggerProcessing();
    console.log(response);
    // log payment response to the backend
    logPayment(response);
}   

// function to log payment response to the backend
function logPayment(response){
    // make a POST request to the backend to log the payment response
    fetch('/log-payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(response),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // if payment is successful, call verifyPayment() to verify the payment
        if(response.status === 'success'){
            verifyPayment(response.reference);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// function to verify payment
function verifyPayment(reference){
    // make a POST request to the backend to verify the payment
    fetch('/verify-payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({reference: reference}),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // if payment is successful, display a success message to the user
        if(data.status === 'success'){
            // display a success message to the user
            alert('Payment successful');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// on close callback
const onClose = function(){
    console.log('Payment closed');
}

// meta data for the payment
const metaData = {
    custom_fields: [
        {
            display_name: '',
            mobile_number: '',
            payment_purpose: '',
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

function triggerPayment(order){
    metaData.custom_fields[0].display_name = order.name;
    metaData.custom_fields[0].mobile_number = order.phone;
    metaData.custom_fields[0].payment_purpose = order.paymentPurposepurpose;
    // Initialize the payment
    const handler = PaystackPop.setup({
        key: order.paystackPublicKey,
        email: order.email,
        amount: order.amount,
        ref: order.reference,
        metadata: metaData,
        callback: callback,
        onClose: onClose
    });

    // Open the Paystack payment modal
    handler.openIframe();
}

