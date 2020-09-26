from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserProfileForm, UserForm


@login_required
def update_profile(request):
    """
    Displays the users profile if the user is logged in,
    handles change request to save updated user info
    """

    profile = request.user.profile

    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST, instance=profile)
        user_form = UserForm(request.POST, instance=request.user)

        if user_profile_form.is_valid() and user_form.is_valid():
            user_profile_form.save()
            user_form.save()
            messages.success(request, 'Profile updated successfully')

    user_profile_form = UserProfileForm(instance=profile)
    user_form = UserForm(instance=request.user)

    context = {
        'user_profile_form': user_profile_form,
        'user_form': user_form
    }

    return render( request, 'profiles/update_profile.html', context)

@login_required
def delete_profile(request):

    if request.method == 'POST':
        request.user.delete()

        messages.success(request, 'Account deleted successfully')
        redirect_url = reverse('index')
        return redirect(redirect_url)

    return render( request, 'profiles/delete_profile.html')


@login_required
def orders(request):
    """ A view to return the cutomer's orders & their status """

    # TODO
    # Get all orders, filtered by customer id
    # sort by date, most recent first

    user_orders = {
        'order1': 'order 1',
        'order2': 'order 2',
    }

    context = {
        'user_orders': user_orders,
    }

    return render(request, 'profiles/orders.html', context)



@login_required
def order(request):
    """ A view to return a specific order """

    # TODO
    # Get all orders, filtered by customer id
    # filter by order_id

    user_order = {
        'order1': 'order 1',
    }

    context = {
        'user_order': user_order,
    }

    return render(request, 'profiles/order.html', context)
