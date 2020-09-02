from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserProfileForm


@login_required
def update_profile(request):
    """
    Displays the users profile if the user is logged in,
    handles change request to save updated user info
    """

    profile = request.user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    form = UserProfileForm(instance=profile)

    context = {
        'form': form
    }

    return render( request, 'profiles/update_profile.html', context)