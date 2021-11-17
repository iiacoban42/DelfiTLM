# Generated by Django 3.2.8 on 2021-11-17 08:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_auto_20211111_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwords',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='passwords',
            name='password',
            field=models.CharField(max_length=120, validators=[django.core.validators.RegexValidator(message='Enter password containing min 8 characters, min 1 upper and lower case letter, 1 number and 1 special character', regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$')]),
        ),
    ]
