from django.shortcuts import render


def fan_art_gallery(request):
    return render(request, 'fan_art/fan_art_gallery.html')
