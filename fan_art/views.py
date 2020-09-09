from django.shortcuts import render

from .models import FanArt


def fan_art_gallery(request):
    """ A view to return all peices of fan art """

    art_list = FanArt.objects.all()

    context = {
        'art_list': art_list
    }

    return render(request, 'fan_art/fan_art_gallery.html', context)
