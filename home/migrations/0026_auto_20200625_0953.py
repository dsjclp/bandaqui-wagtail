# Generated by Django 3.0.6 on 2020-06-25 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_auto_20200625_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='partitionsindexpage',
            name='heading',
            field=models.CharField(default=1, max_length=65),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partitionsindexpage',
            name='subheading',
            field=models.CharField(default=1, max_length=65),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teampage',
            name='heading',
            field=models.CharField(default=1, max_length=65),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teampage',
            name='subheading',
            field=models.CharField(default=1, max_length=65),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videosindexpage',
            name='heading',
            field=models.CharField(default=1, max_length=65),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videosindexpage',
            name='subheading',
            field=models.CharField(default=1, max_length=65),
            preserve_default=False,
        ),
    ]
