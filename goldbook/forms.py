from django import forms

class GoldenForm(forms.Form):
	name = forms.CharField(required=True)
	message = forms.CharField(required=True)
	title = forms.CharField(required=True)
	rate = forms.IntegerField(required=False)