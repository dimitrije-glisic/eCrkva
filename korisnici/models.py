from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
	pass


class Svestenik(models.Model):
	class Meta:
		verbose_name_plural = 'Svestenici'

	user = models.OneToOneField(User,on_delete=models.CASCADE)
	parohija = models.ForeignKey('domacinstvo.Parohija', on_delete=models.CASCADE)


	ime = models.CharField(max_length=30)
	prezime = models.CharField(max_length=30)
	telefon = models.CharField(max_length=30)
	email = models.EmailField()



	def __str__(self):
		return 'Свештеник\n{}'.format(self.ime + ' ' + self.prezime)
