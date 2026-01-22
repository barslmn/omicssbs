from django import forms
from django.forms import widgets
from django.forms.widgets import Textarea, RadioSelect

class Var2TexShadeForm(forms.Form):
    variants = forms.CharField(
        label="Variants (HGVSp)",
        widget=Textarea(attrs={
            'rows': 4, 
            'class': 'form-control',
            'placeholder': 'NP_003385.2:p.His365Arg\nNP_003385.2:p.Ala368Val'
        }),
        help_text="Enter one variant per line or space-separated."
    )
    
    MODE_CHOICES = [
        ('ortholog', 'Ortholog Mode (Compare species)'),
        ('paralog', 'Paralog Mode (Compare gene family)'),
    ]
    mode = forms.ChoiceField(
        choices=MODE_CHOICES, 
        initial='ortholog', 
        widget=RadioSelect,
        label="Comparison Mode"
    )
    
    taxa = forms.CharField(
        label="Taxon Filter / Target",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Default: Homo sapiens'}),
        help_text="Paralog Mode: Target organism (e.g. 'Homo sapiens'). Ortholog Mode: Optional comma-separated list."
    )
    
    max_seqs = forms.IntegerField(
        label="Max Sequences",
        initial=12,
        min_value=2,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    padding = forms.IntegerField(
        label="Zoom Padding (aa)",
        initial=5,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    show_all = forms.BooleanField(
        label="Show Full Alignment",
        required=False,
        initial=False,
        help_text="If checked, ignores zoom padding and shows the entire protein."
    )


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
