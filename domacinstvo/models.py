from django.db import models
# Create your models here.



from korisnici.models import User,Svestenik

from django.utils import timezone




class Adresa(models.Model):
	grad = models.CharField(max_length=20)
	postanski_broj =models.IntegerField(default=0)
	opstina = models.CharField(max_length=20)
	ulica = models.CharField(max_length=30)
	broj = models.IntegerField(default = 0)
	ulaz = models.CharField(max_length=10, null=True,blank=True,default=None)
	broj_stana = models.IntegerField(null=True,blank=True,default=None)

	def __str__(self):
		rez = f"Град: {self.grad} | Поштански број: {self.postanski_broj} | Улица: {self.ulica + ' ' + str(self.broj)}"
		return rez



class Eparhija(models.Model):
	naziv = models.CharField(max_length=50)
	adresa = models.ForeignKey('Adresa', on_delete=models.CASCADE)
	def __str__(self):
		return '{}'.format(self.naziv)

class CrkvenaOpstina(models.Model):
	naziv = models.CharField(max_length=50)
	adresa = models.ForeignKey('Adresa', on_delete=models.CASCADE)

	def __str__(self):
		return '{}'.format(self.naziv)


class Parohija(models.Model):
	naziv = models.CharField(max_length=50)
	ime_paroha = models.CharField(max_length=20)
	prezime_paroha = models.CharField(max_length=20)

	crkvena_opstina = models.ForeignKey('CrkvenaOpstina',on_delete=models.CASCADE)

	def __str__(self):
		return '{}\nParoh: {}'.format(self.naziv,self.ime_paroha + ' ' + self.prezime_paroha)


class Slava(models.Model):
	naziv = models.CharField(max_length=50)
	datum = models.DateField()

	def __str__(self):
		return f'{self.naziv}'

	def __unicode__(self):
		return u'{self.naziv}'

class Domacinstvo(models.Model):
	ime_domacina = models.CharField(max_length=20)
	prezime_domacina = models.CharField(max_length=20)
	slavska_vodica = models.BooleanField()
	vaskrsnja_vodica = models.BooleanField()

	adresa = models.ForeignKey('Adresa',null=True,on_delete=models.SET_NULL)
	slava1 = models.ForeignKey('Slava',related_name='slava1' ,on_delete=models.CASCADE)
	slava2 = models.ForeignKey('Slava', related_name='slava2',null=True,blank=True,default=None, on_delete=models.CASCADE)
	preslava = models.ForeignKey('Slava',related_name='preslava',null=True,blank=True,default=None, on_delete=models.CASCADE)
	svestenik = models.ForeignKey(Svestenik, null=True,on_delete=models.SET_NULL)

	def __str__(self):
		opis = "Домаћин: {}, Слава: {}, Адреса: {}".format(self.ime_domacina + ' ' + self.prezime_domacina, self.slava1.naziv, self.adresa.ulica + ' ' + str(self.adresa.broj))
		#opis=f'{self.ime_domacina} {self.prezime_domacina}'
		return opis


class Osoba(models.Model):
	ime = models.CharField(max_length=20)
	prezime = models.CharField(max_length=20)
	starost = models.PositiveIntegerField(blank=True,null=True)

	class Meta:
		abstract = True


class Ukucanin(Osoba):
	domacinstvo = models.ForeignKey('Domacinstvo',null=True,on_delete=models.SET_NULL)

	def __str__(self):
		return self.ime + ' ' + self.prezime

class UkucaninTemp(Osoba):
	korisnik = models.ForeignKey(User,on_delete=models.CASCADE)
	def __str__(self):
		return self.ime + ' '  + self.prezime

class Nareceni(Osoba):
	domacinstvo = models.ForeignKey('Domacinstvo',null=True,on_delete=models.SET_NULL)

	def __str__(self):
		return self.ime + ' ' + self.prezime

class NareceniTemp(Osoba):
	korisnik = models.ForeignKey(User,on_delete=models.CASCADE)
	def __str__(self):
		return self.ime + ' '  + self.prezime

class Preminuli(Osoba):
	domacinstvo = models.ForeignKey('Domacinstvo',null=True,on_delete=models.SET_NULL)

	def __str__(self):
		return self.ime + ' ' + self.prezime

class PreminuliTemp(Osoba):
	korisnik = models.ForeignKey(User,on_delete=models.CASCADE)
	def __str__(self):
		return self.ime + ' '  + self.prezime




class Dogadjaj(models.Model):
	domacinstvo = models.ForeignKey('Domacinstvo',on_delete=models.CASCADE)

	tip_dogadjaja = models.CharField(max_length=30)
	datum = models.DateField()
	vreme = models.TimeField()
	status = models.BooleanField(default=False)


	def __str__(self):
		return f'{self.tip_dogadjaja}:\n{self.datum}\n{self.vreme}'



class Planer(models.Model):
	svestenik = models.ForeignKey(Svestenik,on_delete=models.CASCADE)

	#mesec-za-prikaz?
	mesec_za_prikaz = models.DateField(default=timezone.now())


	selektovan_datum = models.DateField(default=timezone.now())

