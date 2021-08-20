from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User, Svestenik
from domacinstvo.models import Parohija, Planer

class SvestenikSignUpForm(UserCreationForm):
	ime = forms.CharField(label='Име', max_length=30)
	prezime = forms.CharField(label='Презиме',max_length=30)
	telefon = forms.CharField(label='Телефон', max_length=30)
	email = forms.EmailField()
	parohija = forms.CharField(label='Парохија',max_length=50)

	class Meta(UserCreationForm.Meta):
		model = User

	@transaction.atomic
	def save(self):
		user = super().save(commit=False)
		user.is_active = False
		user.save()
		ime = self.cleaned_data.get('ime')
		prezime = self.cleaned_data.get('prezime')
		telefon = self.cleaned_data.get('telefon')
		email = self.cleaned_data.get('email')
		parohija_naziv = self.cleaned_data.get('parohija')
		parohija = Parohija.objects.get(naziv=parohija_naziv)

		

		svestenik = Svestenik.objects.create(
												user=user,
												parohija=parohija,
												ime = ime,
												prezime = prezime,
												telefon = telefon,
												email = email


		)

		Planer.objects.create(svestenik=svestenik)

		return user