from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password

# Create your models here.

class UsuarioManager(BaseUserManager):
    def create_user(self,username, email, password = None,**extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(
            username = username,
            email = email,
            **extra_fields
        )
        if password:
            user.set_password(password)  # Encriptar la contraseña
        user.save(using=self._db)
        user.save(using = self.db)
        return user
    
    def create_superuser(self,username,email,password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')
        
        superuser = self.create_user(username, email, password, rol=Role.objects.get(name='Conductor'), **extra_fields)
        return superuser

class Usuario(AbstractBaseUser):
    username = models.CharField('Nombre de usuario', unique=True, max_length=100)
    nombres = models.CharField('Nombres', max_length=200, blank=True)
    apellidos = models.CharField('Apellidos', max_length=200, blank=True)
    nacimiento = models.DateField('Fecha de Nacimiento')
    email = models.EmailField('Correo Electronico', max_length=254, unique=True, null=False)
    direccion = models.CharField('Direccion', max_length=200, blank=True)
    usuario_administrador = models.BooleanField(default=False)
    foto_usuario = models.ImageField('Foto de Usuario', upload_to='user_photos/perfil/', blank=True)
    foto_carnet = models.ImageField('Foto de Carnet', upload_to='user_photos/carnet/', blank=True)
    foto_licencia_conducir = models.ImageField('Foto de Licencia de Conducir', upload_to='user_photos/licencia/', blank=True)
    rol = models.ForeignKey("usuarios.Role", verbose_name=("Rol"), on_delete=models.CASCADE, default=1)
    is_superuser = models.BooleanField(default=False)
    privacidad = models.BooleanField('Acepta politicas de privacidad', default=False)

    USERNAME_FIELD = username

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombres', 'apellidos', 'privacidad']

    def __str__(self):
        return f'Usuario: {self.nombres} {self.apellidos}'
    
    def has_perm(self, perm, obj=None):
        return self.usuario_administrador

    def has_module_perms(self, app_label: str):
        return True
    
    @property
    def is_staff(self):
        return self.usuario_administrador

    @is_staff.setter
    def is_staff(self, value):
        self.usuario_administrador = value
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)


class Role(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name