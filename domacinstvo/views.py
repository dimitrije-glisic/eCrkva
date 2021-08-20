from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from collections import defaultdict

from .forms import (
	UkucaninForma,
	NareceniForma,
	PreminuliForma,
)

from .models import (
	Slava,
	Domacinstvo,
	Dogadjaj,
	Planer,
	Adresa,
	Ukucanin,
	UkucaninTemp,
	Nareceni,
	NareceniTemp,
	Preminuli,
	PreminuliTemp
)

from korisnici.models import Svestenik

from calendar import monthrange
import datetime
from django.utils import timezone

from django.http import JsonResponse, HttpResponse
import json

@login_required
def api_grad(request):
	svestenik = Svestenik.objects.get(user=request.user)
	adresa = svestenik.parohija.crkvena_opstina.adresa
	print(adresa.grad, adresa.postanski_broj)
	response = {'grad': adresa.grad, 'postanski_broj': adresa.postanski_broj}
	return JsonResponse(response)

@login_required
def slave(request):
	slave_query_set = Slava.objects.all()
	slave = {slava.id: slava.naziv for slava in slave_query_set}

	return JsonResponse(slave)

@login_required
def api_ukucani_temp(request):
	ukucani_temp_query_set = UkucaninTemp.objects.filter(korisnik=request.user)
	ukucani_temp = {
		ukucanin.id: ukucanin.ime for ukucanin in ukucani_temp_query_set}

	return JsonResponse(ukucani_temp)

@login_required
def api_sacuvaj_ukucanina_temp(request):
	if request.method == 'POST':
		podaci = json.loads(request.body)
		ime = podaci['ime']
		prezime = podaci['prezime']
		starost = int(podaci['starost'])

		u = UkucaninTemp(ime=ime, prezime=prezime,
						 starost=starost, korisnik=request.user)
		u.save()

		return HttpResponse('ok')

@login_required
def api_preminuli_temp(request):
	preminuli_temp_query_set = PreminuliTemp.objects.filter(
		korisnik=request.user)
	preminuli_temp = {
		ukucanin.id: ukucanin.ime for ukucanin in preminuli_temp_query_set}

	return JsonResponse(preminuli_temp)

@login_required
def api_sacuvaj_preminulog_temp(request):
	if request.method == 'POST':
		podaci = json.loads(request.body)
		ime = podaci['ime']
		prezime = podaci['prezime']
		starost = int(podaci['starost'])

		p = PreminuliTemp(ime=ime, prezime=prezime,
						  starost=starost, korisnik=request.user)
		p.save()

		return HttpResponse('ok')

@login_required
def api_nareceni_temp(request):
	nareceni_temp_query_set = NareceniTemp.objects.filter(
		korisnik=request.user)
	nareceni_temp = {
		ukucanin.id: ukucanin.ime for ukucanin in nareceni_temp_query_set}

	return JsonResponse(nareceni_temp)

@login_required
def api_sacuvaj_narecenog_temp(request):
	if request.method == 'POST':
		podaci = json.loads(request.body)
		ime = podaci['ime']
		prezime = podaci['prezime']
		starost = int(podaci['starost'])

		n = NareceniTemp(ime=ime, prezime=prezime,
						 starost=starost, korisnik=request.user)
		n.save()

		return HttpResponse('ok')


@login_required
def api_otkazi_dogadjaj(request):
	if request.method == 'POST':
		podaci = json.loads(request.body)
		id = podaci['id']
		Dogadjaj.objects.filter(pk=id).delete()
		return HttpResponse("OK")

@login_required
def api_potvrdi_dogadjaj(request):
	if request.method == 'POST':
		podaci = json.loads(request.body)
		id = podaci['id']
		dog = Dogadjaj.objects.get(pk=id)
		dog.status = True
		dog.save()

		dom = dog.domacinstvo

		if dog.tip_dogadjaja == 'Васкршња водица':
			dom.vaskrsnja_vodica = True
			dom.save()
		if dog.tip_dogadjaja == 'Славска водица':
			dom.slavska_vodica = True
			dom.save()

		return HttpResponse('Success')


@login_required
def pocetna(request):
	return render(request, "domacinstvo/pocetna.html")


def dodaj_ukucanina(request):
	forma = UkucaninForma()
	context = {
		'forma': forma,
	}
	return render(request, 'domacinstvo/dodaj_ukucanina.html', context)


def dodaj_preminulog(request):
	forma = PreminuliForma()
	context = {
		'forma': forma,
	}
	return render(request, 'domacinstvo/dodaj_preminulog.html', context)


def dodaj_narecenog(request):
	forma = NareceniForma()
	context = {
		'forma': forma
	}
	return render(request, 'domacinstvo/dodaj_narecenog.html', context)


def test(request):
	forma = UkucaninForma()
	if request.method == 'POST':

		if 'konacan_submit' in request.POST:
			# prebaci iz ukucanin_temp u ukucanin
			ukucani_temp = UkucaninTemp.objects.filter(korisnik=request.user)
			for u_temp in ukucani_temp:
				ime = u_temp.ime
				prezime = u_temp.prezime
				starost = u_temp.starost
				u = UkucaninDummy(ime=ime, prezime=prezime, starost=starost)
				u.save()
			ukucani_temp.delete()
			return redirect('test')

		forma = UkucaninForma(request.POST)
		if forma.is_valid():
			ime = forma['ime'].value()
			prezime = forma['prezime'].value()
			starost = forma['starost'].value()
			print(ime, prezime, starost)

			ukucanin = UkucaninTemp(
				ime=ime, prezime=prezime, starost=starost, korisnik=request.user)
			ukucanin.save()

			return redirect('test')

	if request.method == 'GET':
		# maybe delete ukucani_temp
		ukucani_temp = UkucaninTemp.objects.filter(korisnik=request.user)
		for u_temp in ukucani_temp:
			timestamp = u_temp.timestamp + datetime.timedelta(minutes=5)
			now = timezone.now()
			if now > timestamp:
				print('brise se...')
				u_temp.delete()

	ukucani = UkucaninTemp.objects.all()
	context = {
		'forma': forma,
		'ukucani': ukucani
	}

	return render(request, 'test.html', context)


def dodaj_domacinstvo_test(request):
	DomacinstvoFormSet = formset_factory(DomacinstvoForma)
	AdresaFormSet = formset_factory(AdresaForma)
	if request.method == 'POST':
		domacinstvo_form_set = DomacinstvoFormSet(
			request.POST, prefix='domacinstvo')
		adresa_form_set = AdresaFormSet(request.POST, prefix='adresa')

		if domacinstvo_form_set.is_valid() and adresa_form_set.is_valid():
			for dforma in domacinstvo_form_set:
				dforma.save()
			for aforma in adresa_form_set:
				aforma.save()
	else:
		domacinstvo_form_set = DomacinstvoFormSet(prefix='domacinstvo')
		adresa_form_set = AdresaFormSet(prefix='adresa')

	context = {
		'adresa_form_set': adresa_form_set,
		'domacinstvo_form_set': domacinstvo_form_set
	}
	return render(request, 'dodaj_domacinstvo_test.html', context)


@login_required
def dodaj_domacinstvo(request):
	if request.method == 'POST':

		ime = request.POST.get('ime')
		prezime = request.POST.get('prezime')
		slava_naziv = request.POST.get('slava')
		slava = Slava.objects.filter(naziv=slava_naziv).first()
		slavska_vodica = request.POST.get('slavska_vodica')
		vaskrsnja_vodica = request.POST.get('vaskrsnja_vodica')

		# adresa
		grad = request.POST.get('grad')
		pbroj = request.POST.get('postanski_broj')
		ulica = request.POST.get('ulica')
		broj = int(request.POST.get('broj'))
		ulaz = request.POST.get('ulaz')
		broj_stana = request.POST.get('broj_stana')

		if ulaz == '':
			ulaz = None
		if broj_stana == '':
			broj_stana = None
		else:
			broj_stana = int(broj_stana)

		adresa = Adresa(grad=grad, postanski_broj=pbroj, ulica=ulica,
						broj=broj, ulaz=ulaz, broj_stana=broj_stana)
		adresa.save()

		svestenik = Svestenik.objects.get(user=request.user)

		domacinstvo = Domacinstvo(
			ime_domacina=ime,
			prezime_domacina=prezime,
			slava1=slava,
			slavska_vodica=slavska_vodica,
			vaskrsnja_vodica=vaskrsnja_vodica,
			adresa=adresa,
			svestenik=svestenik
		)
		domacinstvo.save()

		# ukucani
		ukucani = UkucaninTemp.objects.filter(korisnik=request.user)
		for u in ukucani:
			ime = u.ime
			prezime = u.prezime
			starost = u.starost

			ukucanin = Ukucanin(ime=ime, prezime=prezime,
								starost=starost, domacinstvo=domacinstvo)
			ukucanin.save()
		# nareceni
		nareceni = NareceniTemp.objects.filter(korisnik=request.user)
		for n in nareceni:
			ime = n.ime
			prezime = n.prezime
			starost = n.starost
			nareceni = Nareceni(ime=ime, prezime=prezime,
								starost=starost, domacinstvo=domacinstvo)
			nareceni.save()

		# preminuli
		preminuli = PreminuliTemp.objects.filter(korisnik=request.user)
		for p in preminuli:
			ime = p.ime
			prezime = p.prezime
			starost = p.starost
			preminuli = Preminuli(ime=ime, prezime=prezime,
								  starost=starost, domacinstvo=domacinstvo)
			preminuli.save()

		messages.success(request, 'Успешно сте додали домаћинство!')
		return redirect('dodaj_domacinstvo')

	else:
		# izbrisi sve UkucaninTemp
		UkucaninTemp.objects.filter(korisnik=request.user).delete()
		NareceniTemp.objects.filter(korisnik=request.user).delete()
		PreminuliTemp.objects.filter(korisnik=request.user).delete()
		return render(request, 'domacinstvo/dodaj_domacinstvo.html')


def napravi_kalendar(datum):
	broj_dana = monthrange(datum.year, datum.month)[1]

	# novo - trenutni datumi
	trenutni_datumi = []
	for i in range(1, broj_dana + 1):
		tdatum = datetime.date(datum.year, datum.month, i)
		trenutni_datumi.append(tdatum)

	prvi_u_mesecu = datetime.date(datum.year, datum.month, 1)
	prvi_dan = prvi_u_mesecu.weekday()
	poslednji_u_mesecu = datetime.date(datum.year, datum.month, broj_dana)
	poslednji_dan = poslednji_u_mesecu.weekday()

	prethodni_datumi = []  # novo
	if prvi_dan != 1:
		# dohvati poslednja {prvi_dan - 1} dana iz proslog
		prethodni_mesec = prvi_u_mesecu - datetime.timedelta(days=1)

		broj_dana = monthrange(prethodni_mesec.year, prethodni_mesec.month)[1]
		for i in range(broj_dana, broj_dana-prvi_dan, -1):
			# dole je novo
			pdatum = datetime.date(prethodni_mesec.year,
								   prethodni_mesec.month, i)
			prethodni_datumi.append(pdatum)

	if prethodni_datumi:
		prethodni_datumi.reverse()

	naredni_datumi = []  # novo
	if poslednji_dan != 7:
		naredni_mesec = poslednji_u_mesecu + datetime.timedelta(days=1)
		for i in range(1, 7 - poslednji_dan):
			# dole je novo
			ndatum = datetime.date(naredni_mesec.year, naredni_mesec.month, i)
			naredni_datumi.append(ndatum)

	svi_datumi = prethodni_datumi + trenutni_datumi + naredni_datumi

	return prethodni_datumi, trenutni_datumi, naredni_datumi


@login_required
def prikazi_planer(request):
	svestenik = Svestenik.objects.get(user=request.user)
	planer = Planer.objects.filter(svestenik=svestenik).first()
	mesec_za_prikaz = planer.mesec_za_prikaz
	selektovan_datum = planer.selektovan_datum

	prethodni, trenutni, naredni = napravi_kalendar(mesec_za_prikaz)
	svi_datumi = prethodni + trenutni + naredni

	idx_prethodnih_datuma = len(prethodni)
	idx_narednih_datuma = len(svi_datumi) - len(naredni)

	if request.method == 'POST':
		if 'prethodni_dan' in request.POST:
			print('datum se smanjuje...')
			selektovan_datum = selektovan_datum - datetime.timedelta(days=1)

		elif 'naredni_dan' in request.POST:
			print('datum se povecava...')
			selektovan_datum = selektovan_datum + datetime.timedelta(days=1)

		planer.selektovan_datum = selektovan_datum
		planer.save()
		return redirect('planer')
	else:
		# dogadjaji za svestenika
		domacinstva = Domacinstvo.objects.filter(svestenik=svestenik)
		dogadjaji_za_svestenika = []
		for domacinstvo in domacinstva:
			dogadjaji_za_domacinstvo = list(Dogadjaj.objects.filter(
				domacinstvo=domacinstvo, datum=selektovan_datum))
			if dogadjaji_za_domacinstvo:
				dogadjaji_za_svestenika = dogadjaji_za_svestenika + dogadjaji_za_domacinstvo
		dogadjaji_za_svestenika.sort(key=lambda x: x.vreme)

		enum_datumi = enumerate(svi_datumi)
		context = {
			'mesec_za_prikaz': mesec_za_prikaz,
			'dogadjaji': dogadjaji_za_svestenika,
			'selektovan_datum': selektovan_datum,
			'idx_prethodnih_datuma': idx_prethodnih_datuma,
			'idx_narednih_datuma': idx_narednih_datuma,
			'enum_datumi': enum_datumi,
		}
		return render(request, 'domacinstvo/planer.html', context=context)


def api_selektuj_datum(request, datum):
	svestenik = Svestenik.objects.get(user=request.user)
	planer = Planer.objects.get(svestenik=svestenik)
	planer.selektovan_datum = datum
	planer.save()

	return redirect('planer')


def api_smanji_mesec(request):
	svestenik = Svestenik.objects.get(user=request.user)
	planer = Planer.objects.get(svestenik=svestenik)
	datum = planer.mesec_za_prikaz
	prvi_u_mesecu = datetime.date(datum.year, datum.month, 1)
	prethodni_mesec = prvi_u_mesecu - datetime.timedelta(days=1)
	planer.mesec_za_prikaz = prethodni_mesec
	planer.save()

	return redirect('planer')


def api_povecaj_mesec(request):
	svestenik = Svestenik.objects.get(user=request.user)
	planer = Planer.objects.get(svestenik=svestenik)
	datum = planer.mesec_za_prikaz
	broj_dana = monthrange(datum.year, datum.month)[1]
	poslednji_u_mesecu = datetime.date(datum.year, datum.month, broj_dana)
	naredni_mesec = poslednji_u_mesecu + datetime.timedelta(days=1)
	planer.mesec_za_prikaz = naredni_mesec
	planer.save()

	return redirect('planer')


@login_required
def pretraga(request):
	svestenik = Svestenik.objects.get(user=request.user)
	d = Domacinstvo.objects.filter(svestenik=svestenik)

	if request.method == 'GET':
		slava = request.GET.get('slava')
		prezime = request.GET.get('prezime')
		ulica = request.GET.get('ulica')
		if slava != '' and slava is not None:
			d = d.filter(slava1__naziv__icontains=slava)
		if prezime != '' and prezime is not None:
			d = d.filter(prezime_domacina__icontains=prezime)
		if ulica != '' and ulica is not None:
			d = d.filter(adresa__ulica__icontains=ulica)

		d = d[:10]
		context = {
			'domacinstva': d
		}

		return render(request, 'domacinstvo/pretraga.html', context)


def pripremi_datum_vreme(datum_vreme):
	temp = datum_vreme.split(' ')
	datum = temp[0]
	vreme = temp[1] + temp[2]
	datum = datetime.datetime.strptime(datum, "%m/%d/%Y").date()
	vreme = datetime.datetime.strptime(vreme, "%I:%M%p").time()
	return datum, vreme


def vreme_start_vreme_end(vreme, vremenski_okvir):
	vreme_datetime = datetime.datetime(1970, 1, 1, vreme.hour, vreme.minute)
	vreme_start = vreme_datetime - datetime.timedelta(minutes=vremenski_okvir)
	vreme_end = vreme_datetime + datetime.timedelta(minutes=vremenski_okvir)
	vreme_start = datetime.time(vreme_start.hour, vreme_start.minute)
	vreme_end = datetime.time(vreme_end.hour, vreme_end.minute)
	return vreme_start, vreme_end

# UVEDI POMOCNE FUNKCIJE


@login_required
def prikazi_domacinstvo(request, id):
	dom = Domacinstvo.objects.filter(id=id).first()
	if request.method == 'POST':
		print('dogadjaj se zakazuje...')
		# prikupi podatke
		tip_dogadjaja = request.POST.get('dogadjaj')
		datum_vreme = request.POST.get('datum')
		datum, vreme = pripremi_datum_vreme(datum_vreme)

		# da li moze tad?
		# check for Dogadjaj in range of +-15min
		vreme_start, vreme_end = vreme_start_vreme_end(vreme, 15)
		d = Dogadjaj.objects.filter(
			datum=datum, vreme__gte=vreme_start, vreme__lte=vreme_end).first()
		if d is None:
			# check for Dogadjaj in range of +-1h
			vreme_start, vreme_end = vreme_start_vreme_end(vreme, 60)
			d = Dogadjaj.objects.filter(
				datum=datum, vreme__gte=vreme_start, vreme__lte=vreme_end).first()
			if d:
				messages.warning(
					request, f'Заказали сте догађај. АЛИ, Догађај [{d} , Домаћинство: {d.domacinstvo}] је близу. Размислите о другом термину!')
			else:
				messages.success(request, 'Успешно сте заказали догађај')
			dogadjaj = Dogadjaj(
				domacinstvo=dom, tip_dogadjaja=tip_dogadjaja, datum=datum, vreme=vreme, status=False)
			dogadjaj.save()
		else:
			messages.error(
				request, f'Догађај није заказан! У то време имате други догађај:[{d} Домаћинство:{d.domacinstvo}]')

		return redirect('prikazi_domacinstvo', id=id)

	else:
		ukucani = Ukucanin.objects.filter(domacinstvo=dom)
		if not ukucani:
			ukucani = []
		nareceni = Nareceni.objects.filter(domacinstvo=dom)
		if not nareceni:
			nareceni = []
		preminuli = Preminuli.objects.filter(domacinstvo=dom)
		if not preminuli:
			preminuli = []
		try:
			dog = Dogadjaj.objects.filter(domacinstvo=dom).order_by('datum', 'vreme')
		except Dogadjaj.DoesNotExist:
			dog = None
		
		context = {
			'domacinstvo': dom,
			'ukucani': enumerate(ukucani),
			'nukucani' : len(ukucani),
			'nareceni': enumerate(nareceni),
			'nnareceni' : len(nareceni),
			'preminuli': enumerate(preminuli),
			'npreminuli': len(preminuli),
			'dogadjaji': dog,
		}
		return render(request, 'domacinstvo/prikazi_domacinstvo.html', context)


# izvestaji


# koliko ima osvescenih vodica a koliko neosvechenih
@login_required
def statistika_svete_vodice(request):
	if request.method == 'GET':
		svestenik = Svestenik.objects.get(user=request.user)
		domacinstva = Domacinstvo.objects.filter(svestenik=svestenik)
		cnt_slavska_ima = 0
		cnt_vaskrsnja_ima = 0
		data = {}
		for d in domacinstva:
			if d.slavska_vodica:
				cnt_slavska_ima += 1
			if d.vaskrsnja_vodica:
				cnt_vaskrsnja_ima += 1

		cnt_slavska_nema = len(domacinstva) - cnt_slavska_ima
		cnt_vaskrsnja_nema = len(domacinstva) - cnt_vaskrsnja_ima
		data['slavska'] = {
			'ima': cnt_slavska_ima,
			'ima_procenat': cnt_slavska_ima/(cnt_slavska_ima + cnt_slavska_nema) * 100,
			'nema': cnt_slavska_nema,
			'nema_procenat': cnt_slavska_nema/(cnt_slavska_ima + cnt_slavska_nema) * 100,
		}
		data['vaskrsnja'] = {
			'ima': cnt_vaskrsnja_ima,
			'ima_procenat': cnt_vaskrsnja_ima/(cnt_vaskrsnja_ima + cnt_vaskrsnja_nema)*100,
			'nema': cnt_vaskrsnja_nema,
			'nema_procenat': cnt_vaskrsnja_nema/(cnt_vaskrsnja_ima + cnt_vaskrsnja_nema)*100,
		}

		return render(request, 'domacinstvo/statistika_svete_vodice.html', data)


@login_required
def statistika_slave(request):
	if request.method == 'GET':
		svestenik = Svestenik.objects.get(user=request.user)
		domacinstva = Domacinstvo.objects.filter(svestenik=svestenik)

		slave_dict = defaultdict(int)

		slave_i_slavske_vodice = defaultdict(int)

		for d in domacinstva:
			slava = d.slava1
			slave_dict[slava.naziv] += 1
			if d.slavska_vodica:
				slave_i_slavske_vodice[slava.naziv] += 1

		data = {
			'slave': sorted(slave_dict.items(), key=lambda item: item[1], reverse=True),
			'ukupno': len(domacinstva),
			'slave_i_slavske_vodice': slave_i_slavske_vodice
		}

		return render(request, 'domacinstvo/statistika_slave.html', data)


@login_required
def izvestaji(request):
	if request.method == 'GET':
		return render(request, 'domacinstvo/izvestaji.html')
