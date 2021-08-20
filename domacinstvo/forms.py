from django import forms


class UkucaninForma(forms.Form):
	ime = forms.CharField(label='Име',max_length=20)
	prezime = forms.CharField(label='Презиме',max_length=20)
	starost = forms.IntegerField(label='Старост')
	

class PreminuliForma(forms.Form):
	ime = forms.CharField(label='Име',max_length=20)
	prezime = forms.CharField(label='Презиме',max_length=20)
	starost = forms.IntegerField(label='Старост')

class NareceniForma(forms.Form):
	ime = forms.CharField(label='Име',max_length=20)
	prezime = forms.CharField(label='Презиме',max_length=20)
	starost = forms.IntegerField(label='Старост')
