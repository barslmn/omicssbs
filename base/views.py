from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "base/index.html")


def notes(request):
    return render(request, "base/notes.html")


def photos(request):
    return render(request, "base/photos.html")
