$(() => {
  /*
  Handle shipping_address toggle checkbox:
  remove required property so we can populate data in the
  create_payment_intent view function
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

  // Disable submit button
  const submitButton = $('#btn-submit')
  submitButton.prop('disabled', true)

  // mounting our created card element
  card.mount('#card-element');

  card.on('change', (event) => {
    console.log(event)

    if (event.complete) {
      $('#card-error').text('')
      submitButton.prop('disabled', false)
    } else if (event.error) {
      $('#card-error').text(event.error.message)
      submitButton.prop('disabled', true)
    }
  })

  // Prevent the default form submit action
  // Calls the function for paying with Stripe
  $('#payment-form').submit((e) => {
    e.preventDefault()

    // Trim the form values
    $(':input').val((_, oldValue) => oldValue.trim())

    // TODO: disable buttons & UI stuff

    /*
    Getting the client secret & save info
    Getting the values from the form
    Posting to create_payment_intent view
    */

    const saveInfo = true
    const postData = {
      'save_info': saveInfo,
    }

    $(':input').each((_, element) => {
      const field = $(element)
      if (field.attr('name') === undefined) return
      if (field.attr('type') === 'checkbox') {
        if (field.is(':checked')) {
          postData[field.attr('name')] = field.val()
        }
      } else {
        postData[field.attr('name')] = field.val()
      }
    })

    const url = '/checkout/create_payment_intent/'

    $.post(url, postData).done((response) => {
      $('#client_secret').val(response.client_secret)
      payWithCard(stripe, card, response.client_secret)
    }).fail((e) => {

      // If error + redirect from validation function
      if (e.responseJSON['redirect']) {
        window.location.replace(e.responseJSON['redirect'])
      }

      $(':input').removeClass('error-field')

      let topmostField = null
      let topmostPosition = null

      for (key in e.responseJSON) {

        // Highlighting each error field + scroll topmost + focuss on topmost
        const inputField = $(`:input[name="${key}"]`)
        inputField.addClass('error-field')
        if (inputField.offset().top < topmostPosition || topmostPosition === null) {
          topmostField = inputField
          topmostPosition = inputField.offset().top
        }
      }

      topmostField[0].scrollIntoView(false)
      topmostField.focus()
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
      .then((result) => {
        if (result.error) {
          $('#card-error').text(result.error.message)
          card.focus()
          // TODO: re-enable the form
        } else {
          $('#payment-form')[0].submit()
        }
      })
  }
})
