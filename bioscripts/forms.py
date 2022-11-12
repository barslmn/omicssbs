from django import forms

class Var2TexShadeForm(forms.Form):
    hgvsp = forms.CharField(label='HGVSp', max_length=100)
