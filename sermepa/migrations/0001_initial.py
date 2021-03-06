# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-11 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SermepaIdTPV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idtpv', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='SermepaResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('Ds_Date', models.DateField()),
                ('Ds_Hour', models.TimeField()),
                ('Ds_SecurePayment', models.IntegerField()),
                ('Ds_MerchantData', models.CharField(max_length=1024)),
                ('Ds_Card_Country', models.IntegerField(blank=True, null=True)),
                ('Ds_Card_Type', models.CharField(blank=True, max_length=1, null=True)),
                ('Ds_Terminal', models.IntegerField()),
                ('Ds_MerchantCode', models.CharField(max_length=9)),
                ('Ds_ConsumerLanguage', models.IntegerField()),
                ('Ds_Response', models.CharField(max_length=4)),
                ('Ds_Order', models.CharField(max_length=12)),
                ('Ds_Currency', models.IntegerField()),
                ('Ds_Amount', models.IntegerField()),
                ('Ds_Signature', models.CharField(max_length=256)),
                ('Ds_AuthorisationCode', models.CharField(max_length=256)),
                ('Ds_TransactionType', models.CharField(max_length=1)),
                ('Ds_Merchant_Identifier', models.CharField(blank=True, max_length=40, null=True)),
                ('Ds_ExpiryDate', models.CharField(blank=True, max_length=4, null=True)),
                ('Ds_Merchant_Group', models.CharField(blank=True, max_length=9, null=True)),
                ('Ds_Card_Number', models.CharField(blank=True, max_length=40, null=True)),
            ],
        ),
    ]
