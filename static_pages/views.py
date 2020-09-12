from django.shortcuts import render


def index(request):
    return render(request, 'static_pages/index.html')


def about(request):
    context = {'current_page': 'about'}
    return render(request, 'static_pages/about.html', context)


def magic_door(request):
    context = {'current_page': 'magic_door'}
    return render(request, 'static_pages/magic_door.html', context)


def parma_ham(request):
    context = {'current_page': 'parma_ham'}
    return render(request, 'static_pages/parma_ham.html', context)
