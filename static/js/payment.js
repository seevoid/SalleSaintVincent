////////////------ Paypal Stuff goes here ------////////////

paypal.Buttons({
  createOrder: function(data, actions) {
    // Set up the transaction
    return actions.order.create({
      purchase_units: [{
        amount: {
          value: 1
        }
      }]
    });
  },
  onApprove: function(data, actions) {
    // Capture the funds from the transaction
    return actions.order.capture().then(function(details) {
      // Show a success message to your buyer
      // alert('Transaction completed by ' + details.payer.name.given_name);
      // Call your server to save the transaction
      fetch('/paypal_success', {
        method: 'post',
        body: JSON.stringify({
          from_paypal: "yes"
        })
      });
      document.location.href = "/paypal_success";
    });
  }
}).render('#paypal-button-container');