# Generated by Django 5.0.6 on 2025-05-20 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appuser',
            options={'permissions': (('puede_vender', 'Puede vender y crear productos'), ('puede_comprar', 'Puede ver y comprar productos'))},
        ),
    ]
