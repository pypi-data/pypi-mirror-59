# Generated by Django 2.2 on 2019-06-15 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparnik_users', '0027_auto_20190526_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('M', 'مرد'), ('F', 'زن')], default='M', max_length=1, verbose_name='Sex'),
        ),
    ]
