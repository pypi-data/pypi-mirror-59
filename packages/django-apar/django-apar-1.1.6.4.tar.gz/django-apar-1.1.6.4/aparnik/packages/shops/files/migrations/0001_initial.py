# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-10-25 15:43


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filefields', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.Product')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('password', models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='\\u06af\\u0630\\u0631\\u0648\\u0627\\u0698\\u0647')),
                ('iv', models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='IV')),
                ('is_preview', models.BooleanField(default=False, verbose_name='Is Preview')),
                ('banner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_file_banner', to='filefields.FileField', verbose_name='Banner Image')),
                ('file_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_file_obj', to='filefields.FileField', verbose_name='\\u067e\\u0631\\u0648\\u0646\\u062f\\u0647')),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': '\\u067e\\u0631\\u0648\\u0646\\u062f\\u0647',
                'verbose_name_plural': 'Files',
            },
            bases=('products.product',),
        ),
    ]
