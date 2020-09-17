$(() => {

  // Shipping address toggle checkbox
  $('#use-card-address-as-shipping-address').change(function () {
    $('#shipping-address-div').toggle();
  })

  // Read stripe details from HTML hidden fields
  const stripePublicKey = $('#stripe_public_key').val()
  const clientSecret = $('#client_secret').val()

  // Creating a new stripe instance
  const stripe = Stripe(stripePublicKey);

  // Stripe's default styling
  const style = {
    base: {
      color: '#000',
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: 'antialiased',
      fontSize: '16px',
      '::placeholder': {
        color: '#aab7c4'
      }
    },
    invalid: {
      color: '#dc3545',
      iconColor: '#dc3545'
    }
  };

  // Creating a new card element on our stripe instance
  const elements = stripe.elements();
  const card = elements.create('card', {style: style});

  // mounting our created card element
  card.mount('#card-element');

})
