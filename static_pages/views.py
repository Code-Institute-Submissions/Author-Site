from django.shortcuts import render


def index(request):
    return render(request, 'static_pages/index.html')


def about(request):
    return render(request, 'static_pages/about.html')


def magic_door(request):
    return render(request, 'static_pages/magic_door.html')


def parma_ham(request):
    return render(request, 'static_pages/parma_ham.html')
