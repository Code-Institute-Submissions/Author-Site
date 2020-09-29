from django.shortcuts import render


def index(request):
    """ View to return home page """
    return render(request, 'static_pages/index.html')


def about(request):
    """ View to return about the author page """
    context = {'current_page': 'about'}
    return render(request, 'static_pages/about.html', context)


def magic_door(request):
    """ View to return about the series 'Magic Door' page """
    context = {'current_page': 'magic_door'}
    return render(request, 'static_pages/magic_door.html', context)


def parma_ham(request):
    """ View to return about the series 'Parma Ham' page """
    context = {'current_page': 'parma_ham'}
    return render(request, 'static_pages/parma_ham.html', context)
