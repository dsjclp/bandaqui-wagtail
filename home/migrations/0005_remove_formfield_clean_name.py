# Generated by Django 3.0.6 on 2020-09-05 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_formfield_clean_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formfield',
            name='clean_name',
        ),
    ]