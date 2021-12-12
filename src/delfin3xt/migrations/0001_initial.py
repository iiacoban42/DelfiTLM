# Generated by Django 3.2.8 on 2021-12-12 18:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ewilgs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delfin3xt_L0_telemetry',
            fields=[
                ('id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='ewilgs.downlink')),
                ('frame_time', models.TimeField(default=datetime.time)),
                ('send_time', models.TimeField(default=datetime.time)),
                ('receive_time', models.TimeField(default=datetime.time)),
                ('radio_amateur', models.IntegerField(default=None, null=True)),
                ('frame', models.BinaryField(default=None, null=True)),
                ('processed', models.BooleanField(default=False)),
                ('frequency', models.FloatField(default=None, null=True)),
                ('qos', models.FloatField(default=None, null=True)),
            ],
        ),
    ]
