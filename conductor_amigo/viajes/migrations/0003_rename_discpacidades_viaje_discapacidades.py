# Generated by Django 4.1.12 on 2023-11-20 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viajes', '0002_viaje_discpacidades_viaje_inicio_alter_viaje_destino'),
    ]

    operations = [
        migrations.RenameField(
            model_name='viaje',
            old_name='discpacidades',
            new_name='discapacidades',
        ),
    ]
