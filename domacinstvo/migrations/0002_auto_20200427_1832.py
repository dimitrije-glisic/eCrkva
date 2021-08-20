# Generated by Django 3.0.5 on 2020-04-27 16:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('domacinstvo', '0001_initial'),
        ('korisnici', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='ukucanintemp',
            name='korisnik',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ukucanin',
            name='domacinstvo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='domacinstvo.Domacinstvo'),
        ),
        migrations.AddField(
            model_name='preminulitemp',
            name='korisnik',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='preminuli',
            name='domacinstvo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='domacinstvo.Domacinstvo'),
        ),
        migrations.AddField(
            model_name='planer',
            name='svestenik',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='korisnici.Svestenik'),
        ),
        migrations.AddField(
            model_name='parohija',
            name='crkvena_opstina',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='domacinstvo.CrkvenaOpstina'),
        ),
        migrations.AddField(
            model_name='narecenitemp',
            name='korisnik',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='nareceni',
            name='domacinstvo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='domacinstvo.Domacinstvo'),
        ),
        migrations.AddField(
            model_name='eparhija',
            name='adresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='domacinstvo.Adresa'),
        ),
        migrations.AddField(
            model_name='domacinstvo',
            name='adresa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='domacinstvo.Adresa'),
        ),
        migrations.AddField(
            model_name='domacinstvo',
            name='preslava',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='preslava', to='domacinstvo.Slava'),
        ),
        migrations.AddField(
            model_name='domacinstvo',
            name='slava1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slava1', to='domacinstvo.Slava'),
        ),
        migrations.AddField(
            model_name='domacinstvo',
            name='slava2',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slava2', to='domacinstvo.Slava'),
        ),
        migrations.AddField(
            model_name='domacinstvo',
            name='svestenik',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='korisnici.Svestenik'),
        ),
        migrations.AddField(
            model_name='dogadjaj',
            name='domacinstvo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='domacinstvo.Domacinstvo'),
        ),
        migrations.AddField(
            model_name='crkvenaopstina',
            name='adresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='domacinstvo.Adresa'),
        ),
    ]
