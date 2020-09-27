/* ON LOAD */
$(() => {
  let forms = {}
  const payButton = $('#pay-button')

  payButton.on('click', event => {
    if (payButton.hasClass('disabled')) event.preventDefault()
  })

  $('form').each(function () {
    let product_id = $(this).find('input[name=product_id]').val()
    let amount_input = $(this).find('input[name=amount]')
    let amount = parseInt(amount_input.val())
    let basket_item = $(this).parents('.basket-item')
    let decrement_button = $(this).find('button[name=decrement]')
    let increment_button = $(this).find('button[name=increment]')

    forms[product_id] = {
      'origional_amount': amount,
      'new_amount': amount,
      'amount_input': amount_input,
      'basket_item': basket_item,
      'decrement_button': decrement_button,
    }

    increment_button.click(() => increment(product_id))
    decrement_button.click(() => decrement(product_id))
    amount_input.change(() => on_input_change(product_id))
  })

  function on_input_change(product_id) {
    forms[product_id]['new_amount'] = Number.parseInt(forms[product_id]['amount_input'].val())
    update(product_id)
  }

  function increment(product_id) {
    forms[product_id]['new_amount'] += 1
    update(product_id)
  }

  function decrement(product_id) {
    forms[product_id]['new_amount'] -= 1
    update(product_id)
  }

  function update(product_id) {
    let origional_amount = forms[product_id]['origional_amount']
    let new_amount = forms[product_id]['new_amount']

    forms[product_id]['amount_input'].val(new_amount)

    if (origional_amount != new_amount) {
      forms[product_id]['basket_item'].addClass('amount-changed')
      payButton.addClass('disabled')
    } else {
      forms[product_id]['basket_item'].removeClass('amount-changed')
      payButton.removeClass('disabled')
    }

    if (new_amount === 0){
      forms[product_id]['basket_item'].addClass('zero')
      forms[product_id]['decrement_button'].prop('disabled', true)
    } else {
      forms[product_id]['basket_item'].removeClass('zero')
      forms[product_id]['decrement_button'].prop('disabled', false)
    }

  }


})

