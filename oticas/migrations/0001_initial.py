# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('data_adc', models.DateTimeField(auto_now_add=True)),
                ('valor_total', models.DecimalField(null=True, max_digits=6, decimal_places=2)),
                ('dono', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EnderecoUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('cep', models.CharField(max_length=8)),
                ('rua', models.CharField(max_length=200)),
                ('numero', models.IntegerField()),
                ('complemento', models.CharField(max_length=20, blank=True)),
                ('bairro', models.CharField(max_length=40)),
                ('cidade', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=2)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Endereço dos Usuários',
            },
        ),
        migrations.CreateModel(
            name='Oculos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('marca', models.CharField(max_length=100)),
                ('modelo', models.CharField(max_length=100)),
                ('estilo', models.CharField(max_length=100)),
                ('material', models.CharField(max_length=100)),
                ('publico', models.CharField(max_length=100)),
                ('sexo', models.CharField(max_length=100)),
                ('prazo', models.CharField(max_length=2)),
                ('valor', models.DecimalField(max_digits=6, decimal_places=2)),
                ('pagamento', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('disp', models.BooleanField(default=True)),
                ('imagem', models.ImageField(upload_to='oticas/fotos')),
                ('img1', models.ImageField(blank=True, upload_to='oticas/fotos')),
                ('img2', models.ImageField(blank=True, upload_to='oticas/fotos')),
                ('img3', models.ImageField(blank=True, upload_to='oticas/fotos')),
                ('data_adc', models.DateTimeField(auto_now_add=True)),
                ('data_upd', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Oculos',
                'ordering': ('-data_adc',),
            },
        ),
        migrations.AddField(
            model_name='carrinho',
            name='produto',
            field=models.ForeignKey(to='oticas.Oculos'),
        ),
    ]
