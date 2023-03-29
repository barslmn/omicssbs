from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "personal/index.html")

def cv_html(request):
    return render(request, "personal/cv.html")
