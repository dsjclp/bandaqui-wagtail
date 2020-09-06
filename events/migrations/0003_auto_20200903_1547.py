# Generated by Django 3.0.6 on 2020-09-03 15:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('events', '0002_auto_20200731_0941'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Instrument non précisé', 'Instrument non précisé'), ('Clarinette sib solo', 'Clarinette sib solo'), ('Clarinette mib', 'Clarinette mib'), ('Clarinette sib 1', 'Clarinette sib 1'), ('Clarinette sib 2', 'Clarinette sib 2'), ('Clarinette sib 3A', 'Clarinette sib 3A'), ('Clarinette sib 3B', 'Clarinette sib 3B'), ('Clarinette sib 4', 'Clarinette sib 4'), ('Clarinette sib 5', 'Clarinette sib 5'), ('Clarinette basse 1A', 'Clarinette basse 1A'), ('Clarinette basse 1B', 'Clarinette basse 1B'), ('Clarinette basse 2', 'Clarinette basse 2'), ('Clarinette alto', 'Clarinette alto'), ('Cor de basset', 'Cor de basset'), ('Contrebasse à cordes', 'Contrebasse à cordes'), ('Trompette', 'Trompette'), ('Caisse claire', 'Caisse claire'), ('Grosse caisse', 'Grosse caisse'), ('Saxophone alto', 'Saxophone alto'), ('Saxophone baryton', 'Saxophone baryton'), ('Saxophone soprano', 'Saxophone soprano'), ('Saxophone ténor', 'Saxophone ténor'), ('Soubassophone', 'Soubassophone'), ('Trombone', 'Trombone')], default='Clarinette sib', max_length=200)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(choices=[('OUI', 'J y serai'), ('NON', 'Je n y serai pas'), ('PEUT-ETRE', 'Je ne suis pas sûr')], default='OUI', max_length=9)),
                ('iswaiting', models.BooleanField(default=False, verbose_name='is waiting status')),
                ('event_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Page')),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instrumentparticipations', to='events.Instrument')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Inscription',
                'verbose_name_plural': 'Inscriptions',
                'ordering': ('instrument',),
            },
        ),
        migrations.AlterField(
            model_name='eventcalpage',
            name='instruments',
            field=models.ManyToManyField(blank=True, help_text='Instruments this event belongs to', through='events.InstrumentEventPage', to='events.Instrument', verbose_name='Instruments'),
        ),
        migrations.AlterField(
            model_name='instrumenteventpage',
            name='instrument',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='events.Instrument', verbose_name='Instrument'),
        ),
    ]