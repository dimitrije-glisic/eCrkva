from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.views.generic import CreateView

from .forms import SvestenikSignUpForm

from domacinstvo.models import Parohija

from .models import User

class SvestenikSignUpView(CreateView):
	model = User
	form_class = SvestenikSignUpForm
	template_name = 'registration/svestenik_signup.html'

	def get_context_data(self,**kwargs):
		kwargs['user_type'] = 'svestenik'
		return super().get_context_data(**kwargs)


	def form_valid(self,form):
		parohija_naziv = form.cleaned_data.get('parohija')
		try:		
			parohija = Parohija.objects.get(naziv=parohija_naziv)
		except:
			form.add_error('parohija','Нисте правилно одабрали парохију')
			return self.form_invalid(form)
		user = form.save()
		return redirect('login')


