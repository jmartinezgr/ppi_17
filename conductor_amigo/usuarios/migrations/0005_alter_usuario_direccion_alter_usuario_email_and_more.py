# Generated by Django 4.1.12 on 2023-10-29 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_usuario_privacidad_alter_usuario_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='direccion',
            field=models.CharField(blank=True, max_length=200, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='foto_carnet',
            field=models.ImageField(blank=True, upload_to='carnet/', verbose_name='Foto de Carnet'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='foto_licencia_conducir',
            field=models.ImageField(blank=True, upload_to='licencia/', verbose_name='Foto de Licencia de Conducir'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='foto_usuario',
            field=models.ImageField(blank=True, upload_to='perfil/', verbose_name='Foto de Usuario'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='privacidad',
            field=models.BooleanField(default=False, verbose_name='Acepta políticas de privacidad'),
        ),
    ]