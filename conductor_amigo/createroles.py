# create_roles.py

import os
import django
from django.conf import settings

# Configura la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conductor_amigo.settings')
django.setup()

from usuarios.models import Role

def create_roles():
    # Crea los roles que necesitas
    Role.objects.get_or_create(name="Pasajero")
    Role.objects.get_or_create(name="Conductor")

if __name__ == '__main__':
    create_roles()
