from django.shortcuts import render, redirect
from django.http import FileResponse, StreamingHttpResponse
from django.conf import settings
import subprocess
import secrets
import csv
import re
import os


from .forms import Var2TexShadeForm, CrossSymbolCheckerForm

# Create your views here.


def index(request):
    return render(request, "bioscripts/index.html")


def brainspan(request):
    return render(request, "bioscripts/brainspan.html")


def prism(request):
    return render(request, "bioscripts/prism.html")

def var2texshade(request):
    if request.method == "POST":
        form = Var2TexShadeForm(request.POST)
        if form.is_valid():
            # 1. Extract Data
            raw_variants = form.cleaned_data["variants"]
            # Normalize newlines/commas to list
            variants_list = re.split(r'[\s,]+', raw_variants.strip())
            
            mode = form.cleaned_data["mode"]
            taxa = form.cleaned_data["taxa"]
            max_seqs = form.cleaned_data["max_seqs"]
            padding = form.cleaned_data["padding"]
            show_all = form.cleaned_data["show_all"]

            # 2. Setup Paths
            module_path = settings.BASE_DIR.parent.joinpath("bioscripts/modules/var2texshade/var2texshade.py")
            # Create a safe temp filename
            output_filename = f"alignment_{secrets.token_hex(4)}.pdf"
            output_path = os.path.join("/tmp", output_filename)

            # 3. Construct Command (List format is safer than shell=True)
            # We use 'tsp -fn' to run in foreground but queue the slot
            cmd = ["tsp", "-fn", "python3", str(module_path)]
            
            # Append Variants
            cmd.extend(variants_list)
            
            # Append Options
            cmd.extend(["--output", output_path])
            cmd.extend(["--mode", mode])
            if taxa:
                cmd.extend(["--taxa", taxa])
            cmd.extend(["--max_seqs", str(max_seqs)])
            cmd.extend(["--padding", str(padding)])
            if show_all:
                cmd.append("--show_all")

            # 4. Execute
            try:
                # check_output captures stdout/stderr if needed
                subprocess.check_output(cmd, stderr=subprocess.STDOUT)
                
                # 5. Return File
                if os.path.exists(output_path):
                    return FileResponse(
                        open(output_path, "rb"),
                        as_attachment=True,
                        filename="variant_alignment.pdf"
                    )
                else:
                    return render(request, "bioscripts/var2texshade.html", {
                        "form": form, 
                        "error": "Error: Output file was not generated."
                    })
            except subprocess.CalledProcessError as e:
                # Decode error output for debugging
                err_msg = e.output.decode('utf-8') if e.output else str(e)
                return render(request, "bioscripts/var2texshade.html", {
                    "form": form, 
                    "error": f"Processing Error: {err_msg}"
                })

    else:
        form = Var2TexShadeForm()

    return render(request, "bioscripts/var2texshade.html", {"form": form})


def var2texshade_api(request, hgvsp):
    module_path = settings.BASE_DIR.parent.joinpath("bioscripts/modules/var2texshade/")
    try:
        result = subprocess.check_output(
            f"tsp -fn {module_path.joinpath('var2texshade.sh')} {hgvsp}", shell=True
        )
    except subprocess.CalledProcessError as E:
        return render(
            request,
            "bioscripts/var2texshade.html",
            {"error": f"Error: {E.output.decode('utf-8')}"},
        )
    return FileResponse(
        open(result.decode("utf-8").strip(), "rb"),
        as_attachment=True,
        filename=f"{hgvsp}.pdf",
    )


def crosssymbolchecker(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = CrossSymbolCheckerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            symbols = form.cleaned_data["symbols"]
            assembly = form.cleaned_data["assembly"]
            source = form.cleaned_data["source"]
            symbols = symbols.replace("\r\n", " ")

            # Process
            module_path = settings.BASE_DIR.parent.joinpath(
                "bioscripts/modules/cross-symbol-checker/"
            )
            label = secrets.token_urlsafe(6)
            subprocess.run(
                f"tsp -L {label} {module_path.joinpath('check-geneset.sh')} -s {source} -a {assembly} {symbols}",
                shell=True,
            )
            return redirect("bioscripts:crosssymbolchecker_result", label=label)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CrossSymbolCheckerForm(
            initial={"symbols": "ADA2\nLOC102724070\nMDR1\nSHFM6\nGSTT1\nFAM126A"}
        )

    return render(request, "bioscripts/crosssymbolchecker.html", {"form": form})


def crosssymbolchecker_result(request, label):
    try:
        status, filename = (
            subprocess.check_output(
                f"tsp -l | grep {label} | awk '{{print $2\" \"$3}}'", shell=True
            )
            .decode("utf-8")
            .split()
        )
    except ValueError:
        return render(
            request,
            "bioscripts/crosssymbolchecker_result.html",
            {"label": label, "status": "error"},
        )
    if request.method == "POST":
        try:
            return StreamingHttpResponse(
                (line for line in open(filename).read()),
                content_type="text/plain",
                headers={
                    "Content-Disposition": f'attachment; filename="omicssbs_genesetchecker_{label}.txt"'
                },
            )
        except FileNotFoundError:
            return render(
                request,
                "bioscripts/crosssymbolchecker_result.html",
                {"label": label, "status": "error"},
            )
    return render(
        request,
        "bioscripts/crosssymbolchecker_result.html",
        {"status": status, "label": label},
    )


##############################
##     HGNC VERSION APP     ##
##############################

if os.environ.get("DJANGO_DEBUG"):
    hgnc_data_path = "/home/bar/Desktop/Workbench"
else:
    hgnc_data_path = "/mnt/blockstorage"

#####################
##     helpers     ##
#####################


def left_join_lists(list1, list2):
    joined_list = []

    for sublist1 in list1:
        joined_sublist = sublist1.copy()

        for sublist2 in list2:
            if sublist1[:2] == sublist2[:2]:
                joined_sublist.extend(sublist2[2:])
                break
        joined_list.append(joined_sublist)

    return joined_list


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def get_heatmap_data(request, hgnc_id):
    cmd = f'git --git-dir {os.path.join(hgnc_data_path, "hgnc-data.git")} log -p --name-status --pretty="%d" -- HGNC:{hgnc_id}'

    data = subprocess.check_output(cmd, shell=True).decode("utf-8")

    pattern = re.compile(r"\(tag: (\d{4}-\d{2}-\d{2})\)|(\S+)\s+(\S+)")

    name_status = []
    current_group = None
    for line in data.splitlines():
        match = pattern.search(line)
        if match:
            if match.group(1):
                current_group = match.group(1)
            else:
                file_name = match.group(3).split("/")[-1]
                value = match.group(2)
                name_status.append([current_group, file_name, value])

    cmd = rf'git --git-dir {os.path.join(hgnc_data_path, "hgnc-data.git")} log -p  --pretty="%d" -- HGNC:{hgnc_id} | grep -v "^index\|^---\|^+++\|No newline \|^@\|^new"| sed "/^\s*$/d"'
    data = subprocess.check_output(cmd, shell=True).decode("utf-8")
    pattern = re.compile(
        r"\(tag: (\d{4}-\d{2}-\d{2})\)|(diff --git \S+\s+\S+)|(^\+|^-)"
    )
    diffs = []
    current_group = None
    for line in data.splitlines():
        match = pattern.search(line)
        if match:
            if match.group(1):
                current_group = match.group(1)
            elif match.group(2):
                file_name = match.group(2).split("/")[-1]
                diffs.append([current_group, file_name, []])
            elif match.group(3):
                diffs[-1][2].append(line)
    diffs = [[diff[0], diff[1], "\n".join(diff[2])] for diff in diffs]

    # Process the data
    header = ["group", "variable", "value", "diff"]
    rows = left_join_lists(name_status, diffs)
    rows.insert(0, header)

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    return StreamingHttpResponse(
        (writer.writerow(row) for row in rows),
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="HGNC:{hgnc_id}.csv"'},
    )


##########################
##    view functions    ##
##########################


def hgnc_version(request):

    hgnc_lookup_path = os.path.join(hgnc_data_path, "hgnc_lookup")
    with open(hgnc_lookup_path) as f:
        hgnc_lookup = {
            line.split("\t")[0]: line.split("\t")[1] for line in f.read().splitlines()
        }
    return render(
        request,
        "bioscripts/hgnc_version.html",
        {"hgnc_lookup": hgnc_lookup},
    )
