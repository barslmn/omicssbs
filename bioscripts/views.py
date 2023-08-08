from django.shortcuts import render, redirect
from django.http import FileResponse, StreamingHttpResponse
from django.conf import settings
import subprocess
import secrets

from .forms import Var2TexShadeForm, CrossSymbolCheckerForm
# Create your views here.

def index(request):
    return render(request, 'bioscripts/index.html')

def prism(request):
    return render(request, 'bioscripts/prism.html')

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
        result = subprocess.check_output(f"tsp -fn {module_path.joinpath('var2texshade.sh')} {hgvsp}", shell=True)
    except subprocess.CalledProcessError as E:
        return render(request,
                      'bioscripts/var2texshade.html',
                      {"error": f"Error: {E.output.decode('utf-8')}"})
    return FileResponse(open(result.decode('utf-8').strip(), 'rb'), as_attachment=True, filename=f'{hgvsp}.pdf')


def crosssymbolchecker(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CrossSymbolCheckerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            symbols = form.cleaned_data['symbols']
            assembly = form.cleaned_data['assembly']
            source = form.cleaned_data['source']
            symbols = symbols.replace("\r\n", " ")

            # Process
            module_path = settings.BASE_DIR.parent.joinpath("bioscripts/modules/cross-symbol-checker/")
            label = secrets.token_urlsafe(6)
            subprocess.run(f"tsp -L {label} {module_path.joinpath('check-geneset.sh')} -s {source} -a {assembly} {symbols}", shell=True)
            return redirect("bioscripts:crosssymbolchecker_result", label=label)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CrossSymbolCheckerForm(initial={'symbols': 'ADA2\nLOC102724070\nMDR1\nSHFM6\nGSTT1\nFAM126A'})

    return render(request, 'bioscripts/crosssymbolchecker.html', {'form': form})


def crosssymbolchecker_result(request, label):
    try:
        status, filename = subprocess.check_output(f"tsp -l | grep {label} | awk '{{print $2\" \"$3}}'", shell=True).decode('utf-8').split()
    except ValueError:
        return render(request,
                    'bioscripts/crosssymbolchecker_result.html',
                    {"label": label, "status": "error"})
    if request.method == 'POST':
        try:
            return StreamingHttpResponse(
                (line for line in open(filename).read()),
                content_type="text/plain",
                headers={'Content-Disposition': f'attachment; filename="omicssbs_genesetchecker_{label}.txt"'},
            )
        except FileNotFoundError:
            return render(request,
                        'bioscripts/crosssymbolchecker_result.html',
                          {"label": label, "status": "error"})
    return render(request,
                'bioscripts/crosssymbolchecker_result.html',
                    {"status": status, "label": label})
