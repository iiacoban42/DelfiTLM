# Generated by Django 3.2.8 on 2022-02-05 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ewilgs', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TLE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField()),
                ('sat', models.CharField(max_length=70)),
                ('tle', models.TextField()),
            ],
        ),
    ]
