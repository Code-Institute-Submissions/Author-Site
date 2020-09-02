from django.shortcuts import render

def index(request):
    return render(request, 'static_pages/index.html')

def about(request):
    return render(request, 'static_pages/about.html')
