# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-01 12:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Abode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[(b'SH', b'Small house'), (b'H', b'House'), (b'SB', b'Small building'), (b'B', b'Building')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Citizen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('middle_name', models.CharField(blank=True, default=b'', max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('birth', models.DateField()),
                ('gender', models.CharField(choices=[(b'M', b'Male'), (b'F', b'Female')], max_length=1)),
                ('abode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citizens', to='demo.Abode')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Hobby',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('citizens', models.ManyToManyField(to='demo.Citizen')),
            ],
        ),
        migrations.CreateModel(
            name='World',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField(blank=True, default=b'')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='world',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='demo.World'),
        ),
        migrations.AddField(
            model_name='abode',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abodes', to='demo.City'),
        ),
        migrations.AddField(
            model_name='abode',
            name='owner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_abode', to='demo.Citizen'),
        ),
    ]