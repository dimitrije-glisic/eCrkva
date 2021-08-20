from django.urls import path, register_converter

from . import views
import datetime

class DateConverter:
	regex = r'\d{4}-\d{2}-\d{2}'

	def to_python(self,value):
		return datetime.datetime.strptime(value,'%Y-%m-%d')

	def to_url(self,value):
		return value

register_converter(DateConverter,'yyyy')


urlpatterns = [
	path('dodaj_ukucanina/',views.dodaj_ukucanina,name='dodaj_ukucanina'),
	path('dodaj_preminulog/',views.dodaj_preminulog,name='dodaj_preminulog'),
	path('dodaj_narecenog/',views.dodaj_narecenog,name='dodaj_narecenog'),

	path('dodaj_domacinstvo_test/',views.dodaj_domacinstvo_test,name='dodaj_domacinstvo_test'),


	path('test/',views.test,name='test'),
	path('dodaj_domacinstvo/',views.dodaj_domacinstvo,name='dodaj_domacinstvo'),
	path('planer/',views.prikazi_planer,name='planer'),
	path('',views.pocetna, name='domacinstvo-pocetna'),
	path('pretraga/',views.pretraga,name='pretraga'),
	path('domacinstvo/<int:id>',views.prikazi_domacinstvo,name='prikazi_domacinstvo'),


	#api
	path('slave/',views.slave, name='slave'),
	path('api_ukucani_temp/',views.api_ukucani_temp,name='api_ukucani_temp'),
	path('api_sacuvaj_ukucanina_temp/',views.api_sacuvaj_ukucanina_temp,name="api_sacuvaj_ukucanina_temp"),
	
	path('api_nareceni_temp/',views.api_nareceni_temp,name='api_nareceni_temp'),
	path('api_sacuvaj_narecenog_temp/',views.api_sacuvaj_narecenog_temp,name="api_sacuvaj_narecenog_temp"),
	
	path('api_preminuli_temp/',views.api_preminuli_temp,name='api_preminuli_temp'),
	path('api_sacuvaj_preminulog_temp/',views.api_sacuvaj_preminulog_temp,name="api_sacuvaj_preminulog_temp"),
	

	path('api_otkazi_dogadjaj/',views.api_otkazi_dogadjaj,name='api_otkazi_dogadjaj'),
	path('api_potvrdi_dogadjaj/',views.api_potvrdi_dogadjaj,name='api_potvrdi_dogadjaj'),

	path('api_grad/',views.api_grad,name='api_grad'),

	path('api_smanji_mesec',views.api_smanji_mesec,name='api_smanji_mesec'),
	path('api_povecaj_mesec',views.api_povecaj_mesec,name='api_povecaj_mesec'),
	path('api_selektuj_datum/<yyyy:datum>',views.api_selektuj_datum,name='api_selektuj_datum'),

	#izvestaji

	path('statistika_svete_vodice/', views.statistika_svete_vodice, name='statistika_svete_vodice'),
	path('statistika_slave/',views.statistika_slave,name='statistika_slave'),

	path('izvestaji/',views.izvestaji,name='izvestaji'),

]