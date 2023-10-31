# Este código hace uso de funcionalidades proporcionadas por Django,
# un framework de desarrollo web de código abierto. Utiliza modelos
# personalizados para gestionar usuarios y sus roles.

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password


class UsuarioManager(BaseUserManager):
    """
    Manager personalizado para el modelo de usuario.

    Este manager permite crear usuarios regulares y superusuarios.
    """

    def create_user(self, username, email, password=None, incapacidad='ninguna', bibliografia='', calificacion=3, **extra_fields):
        """
        Crea y guarda un usuario regular.

        Args:
            username (str): Nombre de usuario.
            email (str): Correo electrónico del usuario.
            password (str): Contraseña del usuario (opcional).
            incapacidad (str): Valor de incapacidad (por defecto 'ninguna').
            bibliografia (str): Bibliografía del usuario (opcional).
            calificacion (decimal): Calificación del usuario (opcional, valor predeterminado 3).
            extra_fields (dict): Campos adicionales.

        Returns:
            User: Usuario creado.
        """
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            incapacidad=incapacidad,
            bibliografia=bibliografia,
            calificacion=calificacion,
            **extra_fields
        )
        if password:
            user.set_password(password)  # Encriptar la contraseña
        user.save(using=self._db)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, password=None, incapacidad='ninguna', bibliografia='', calificacion=3, **extra_fields):
        """
        Crea y guarda un superusuario.

        Args:
            username (str): Nombre de usuario.
            email (str): Correo electrónico del usuario.
            password (str): Contraseña del superusuario (opcional).
            incapacidad (str): Valor de incapacidad (por defecto 'ninguna').
            bibliografia (str): Bibliografía del usuario (opcional).
            calificacion (decimal): Calificación del usuario (opcional, valor predeterminado 3).
            extra_fields (dict): Campos adicionales.

        Returns:
            User: Superusuario creado.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        superuser = self.create_user(username, email, password, incapacidad, bibliografia, calificacion, rol=Role.objects.get(name='Conductor'), **extra_fields)
        return superuser



class Usuario(AbstractBaseUser):
    """
    Modelo de usuario personalizado.

    Este modelo extiende la funcionalidad de AbstractBaseUser y PermissionsMixin para usuarios.
    """
    username = models.CharField('Nombre de usuario', 
                                unique=True, 
                                max_length=100)
    nombres = models.CharField('Nombres', 
                               max_length=200, 
                               blank=True)
    apellidos = models.CharField('Apellidos', 
                                 max_length=200, 
                                 blank=True)
    nacimiento = models.DateField('Fecha de Nacimiento')
    email = models.EmailField('Correo Electrónico', 
                              max_length=254, 
                              unique=True, 
                              null=False)
    direccion = models.CharField('Dirección', max_length=200, blank=True)
    usuario_administrador = models.BooleanField(default=False)
    foto_usuario = models.ImageField('Foto de Usuario', 
                                     upload_to='perfil/', 
                                     blank=True)
    foto_carnet = models.ImageField('Foto de Carnet', 
                                    upload_to='carnet/', 
                                    blank=True)
    foto_licencia_conducir = models.ImageField('Foto de Licencia de Conducir', 
                                               upload_to='licencia/', 
                                               blank=True)
    rol = models.ForeignKey("usuarios.Role", 
                            verbose_name=("Rol"), 
                            on_delete=models.CASCADE, 
                            default=1)
    is_superuser = models.BooleanField(default=False)
    
    privacidad = models.BooleanField('Acepta políticas de privacidad', 
                                     default=False)


    INCAPACIDAD_CHOICES = [
        ('ninguna', 'Ninguna'),
        ('silla_de_ruedas', 'Silla de ruedas'),
        ('muletas', 'Muletas'),
        ('vision_reducida', 'Visión reducida'),
    ]

    # Agrega el campo de incapacidad con las opciones definidas
    incapacidad = models.CharField(
        'Incapacidad',
        max_length=15,
        choices=INCAPACIDAD_CHOICES,
        default='ninguna'  # Valor predeterminado: Ninguna
    )

    bibliografia = models.TextField(
        'Bibliografía', 
        blank=True
        )
    calificacion = models.DecimalField(
        'Calificación', 
        default=5,
        max_digits=3,
        decimal_places=1, 
        validators=[
            MinValueValidator(1), 
            MaxValueValidator(5)
            ]
        )

    USERNAME_FIELD = 'username'

    objects = UsuarioManager()

    REQUIRED_FIELDS = ['email', 'nombres', 'apellidos', 'privacidad']

    def __str__(self):
        """
        Devuelve una representación en cadena del usuario.

        Returns:
            str: Nombre completo del usuario.
        """
        return f'Usuario: {self.nombres} {self.apellidos}'
    
    def has_perm(self, perm, obj=None):
        """
        Verifica si el usuario tiene un permiso específico.

        Args:
            perm (str): Permiso a verificar.
            obj: Objeto al que se aplica el permiso (opcional).

        Returns:
            bool: True si el usuario tiene el permiso, False en caso contrario.
        """
        return self.usuario_administrador

    def has_module_perms(self, app_label: str):
        """
        Verifica si el usuario tiene permisos para acceder a un módulo específico.

        Args:
            app_label (str): Nombre del módulo.

        Returns:
            bool: True si el usuario tiene permisos para el módulo, False en caso contrario.
        """
        return True
    
    @property
    def is_staff(self):
        """
        Verifica si el usuario es miembro del personal.

        Returns:
            bool: True si el usuario es miembro del personal, False en caso contrario.
        """
        return self.usuario_administrador

    @is_staff.setter
    def is_staff(self, value):
        """
        Establece si el usuario es miembro del personal.

        Args:
            value (bool): True si el usuario es miembro del personal, False en caso contrario.
        """
        self.usuario_administrador = value
    
    def set_password(self, raw_password):
        """
        Establece la contraseña del usuario.

        Args:
            raw_password (str): Contraseña sin cifrar.
        """
        self.password = make_password(raw_password)


class Role(models.Model):
    """
    Modelo de roles de usuario.

    Define los roles que un usuario puede tener.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """
        Metodo que retorna el valor toString del modelo
        Returns:
            String: El valor name de la clase.
        """
        return self.name
