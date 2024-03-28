from django import forms
from django.forms import widgets
from django.forms.widgets import Textarea


class Var2TexShadeForm(forms.Form):
    hgvsp = forms.CharField(label="HGVSp", max_length=100)


class CrossSymbolCheckerForm(forms.Form):
    assemblies = [
        ("GRCh37", "GRCh37"),
        ("GRCh38", "GRCh38"),
        ("T2T", "T2T"),
    ]

    sources = [
        ("Ensembl", "Ensembl"),
        ("RefSeq", "RefSeq"),
    ]

    source = forms.ChoiceField(label="Annotation Source", choices=sources)
    assembly = forms.ChoiceField(label="Genome Assembly", choices=assemblies)
    symbols = forms.CharField(label="Gene Symbols", widget=Textarea())
