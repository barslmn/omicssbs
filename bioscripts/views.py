from django.shortcuts import render, redirect
from django.http import FileResponse
from django.conf import settings
from pathlib import Path
import subprocess

from .forms import Var2TexShadeForm
# Create your views here.

def index(request):
    return render(request, 'bioscripts/index.html')

def var2texshade(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Var2TexShadeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            hgvsp = form.cleaned_data['hgvsp']
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return redirect("bioscripts:var2texshade_api", hgvsp=hgvsp)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Var2TexShadeForm()

    return render(request, 'bioscripts/var2texshade.html', {'form': form})


def var2texshade_api(request, hgvsp):
    module_path = settings.BASE_DIR.parent.joinpath("bioscripts/modules/var2texshade/")
    try:
        result = subprocess.check_output(f"{module_path.joinpath('var2texshade.sh')} {hgvsp}", shell=True)
    except subprocess.CalledProcessError as E:
        return render(request,
                      'bioscripts/var2texshade.html',
                      {"error": f"Error: {E.output.decode('utf-8')}"})
    return FileResponse(open(f"{module_path.joinpath(f'{hgvsp}.pdf')}", 'rb'), as_attachment=True, filename=f'{hgvsp}.pdf')
