$(() => {
  /*
  Handle shipping_address toggle checkbox:
  remove required property so we can populate data in the
  validate_form_and_update_payment_intent view function
  */
  const shippingFields = $(':input[name^="shipping_"][required]')

  $('#use-card-address-as-shipping-address').change(function () {
    $('#shipping-address-div').toggle();

    if ($('#use-card-address-as-shipping-address').is(':checked')) {
      shippingFields.prop("required", false)
    } else {
      shippingFields.prop("required", true)
    }

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

  // Prevent the default form submit action
  // Calls the function for paying with Stripe
  $('#payment-form').submit((e) => {
    e.preventDefault()

    // Trim the form values
    $(':input').val((_, oldValue) => oldValue.trim())

    // TODO: disable buttons & UI stuff
    // TODO: capture whether user wants to save their details

    /*
    Getting the client secret & save info
    Getting the values from the form
    Posting to validate_form_and_update_payment_intent view
    */

    // const saveInfo = Boolean($('#id-save-info').attr('checked'))
    const saveInfo = true
    const postData = {
      'client_secret': clientSecret,
      'save_info': saveInfo,
    }

    $(':input').each((_, element) => {
      const field = $(element)
      if (field.attr('name') === undefined) return
      if (field.attr('type') === 'checkbox') {
        postData[field.attr('name')] = field.is(':checked')
      } else {
        postData[field.attr('name')] = field.val()
      }
    })

    const url = '/checkout/validate/'

    $.post(url, postData).done(function () {
      payWithCard(stripe, card, clientSecret)
    }).fail(function() {
      // Reloading page - django will post the error message automatically
      //location.reload();
    })

  })

  // Submit the payment to stripe & handle success / error
  const payWithCard = (stripe, card, clientSecret) => {
    // loading(true)
    stripe
      .confirmCardPayment(clientSecret, {
        payment_method: {
          card: card,
          billing_details: {
            name: $(':input[name="full_name"]').val(),
            phone: $(':input[name="phone_number"]').val(),
            email: $(':input[name="email"]').val(),
            address:{
                line1: $(':input[name="payment_street_address1"]').val(),
                line2: $(':input[name="payment_street_address2"]').val(),
                city: $(':input[name="payment_town_or_city"]').val(),
                country: $(':input[name="payment_country"]').val(),
                state: $(':input[name="payment_county"]').val(),
                postal_code: $(':input[name="payment_postcode"]').val(),
            }
          }
        }
      })
      .then(function(result) {
        if (result.error) {
          // TODO: show error message, re-enable the form
          // showError(result.error.message)
        } else {
          // orderComplete(result.paymentIntent.id)
          console.log('Sucess!')
          /*
          if (result.paymentIntent.status === 'succeeded') {
            form.submit();
          }
          */

        }
      })
  }
})
