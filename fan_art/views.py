from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import FanArt
from profiles.models import UserProfile
from .forms import UserFanArtForm

def fan_art_gallery(request):
    """ A view to return all peices of fan art """

    art_list = FanArt.objects.all()

    context = {
        'art_list': art_list
    }

    return render(request, 'fan_art/fan_art_gallery.html', context)


def user_gallery(request):
    """ A view to return the user's submitted fan art """

    users_art = FanArt.objects.all().filter(user_profile=request.user.id)

    context = {
        'users_art': users_art
    }

    return render(request, 'fan_art/user_art_gallery.html', context)


@login_required
def add_art(request):
    """ A view for the user to submit their own art to the gallery """

    add_art_form = UserFanArtForm()

    context = {
        'add_art_form':  add_art_form,
    }

    return render(request, 'fan_art/add_fan_art.html', context)
