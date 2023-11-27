# Este código hace uso de funcionalidades proporcionadas por Django,
# un framework de desarrollo web de código abierto. Utiliza modelos
# personalizados para gestionar usuarios y sus roles.

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.conf import settings

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

    promedio_manejo = models.FloatField(default=0)
    promedio_higiene = models.FloatField(default=0)
    promedio_charla = models.FloatField(default=0)
    promedio_puntualidad = models.FloatField(default=0)
    promedio_general = models.FloatField(default=0)

    def actualizar_promedios(self):
        """
        Actualiza los promedios del usuario basado en sus calificaciones.

        Obtener todas las calificaciones para el usuario, calcular sumas y conteos por categoría,
        calcular promedios y actualizar en el objeto usuario.
        """
        # Obtener todas las calificaciones para el usuario
        calificaciones = Calificacion.objects.filter(calificado=self)

        # Inicializar sumas y conteos para calcular promedios
        suma_manejo = suma_higiene = suma_charla = suma_puntualidad = suma_general = 0
        conteo_manejo = conteo_higiene = conteo_charla = conteo_puntualidad = conteo_general = 0

        # Calcular sumas y conteos por categoría
        for calificacion in calificaciones:
            if calificacion.categoria == 'Manejo':
                suma_manejo += int(calificacion.calificacion)
                conteo_manejo += 1
            elif calificacion.categoria == 'Higiene del vehiculo':
                suma_higiene += int(calificacion.calificacion)
                conteo_higiene += 1
            elif calificacion.categoria == 'Buena Charla':
                suma_charla += int(calificacion.calificacion)
                conteo_charla += 1
            elif calificacion.categoria == 'Puntualidad':
                suma_puntualidad += int(calificacion.calificacion)
                conteo_puntualidad += 1
            elif calificacion.categoria == 'General':
                suma_general += int(calificacion.calificacion)
                conteo_general += 1

        # Calcular promedios y actualizar en el usuario
        self.promedio_manejo = suma_manejo / conteo_manejo if conteo_manejo != 0 else 0
        self.promedio_higiene = suma_higiene / conteo_higiene if conteo_higiene != 0 else 0
        self.promedio_charla = suma_charla / conteo_charla if conteo_charla != 0 else 0
        self.promedio_puntualidad = suma_puntualidad / conteo_puntualidad if conteo_puntualidad != 0 else 0
        self.promedio_general = suma_general / conteo_general if conteo_general != 0 else 0

        # Guardar cambios en el usuario
        self.save()


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


class Calificacion(models.Model):
    # Definición de las opciones de calificación
    CALIFICACION_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]

    # Definición de las opciones de categoría
    OPCIONES_CHOICES = [
        ('Manejo', 'Manejo'),
        ('Higiene', 'Higiene del vehículo'),
        ('Charla', 'Buena Charla'),
        ('Puntualidad', 'Puntualidad'),
        ('General', 'General'),
    ]

    # Definición de las opciones de categoría para conductores
    CONDUCTOR_CATEGORIA_CHOICES = [
        ('Manejo', 'Manejo'),
        ('Higiene', 'Higiene del vehículo'),
        ('Charla', 'Buena Charla'),
        ('Puntualidad', 'Puntualidad'),
        ('General', 'General'),
    ]

    # Definición de las opciones de categoría para pasajeros
    PASAJERO_CATEGORIA_CHOICES = [
        ('Charla', 'Buena charla'),
        ('Puntualidad', 'Puntualidad'),
        ('General', 'General'),
    ]

    # Campos del modelo
    calificador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='calificador')
    calificado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='calificado')
    categoria = models.CharField(max_length=50, choices=OPCIONES_CHOICES)
    calificacion = models.CharField(max_length=1, choices=CALIFICACION_CHOICES)

    def __str__(self):
        # Representación en cadena del objeto
        return f'{self.calificador} calificó a {self.calificado} en {self.categoria} con {self.calificacion} puntos'

    def save(self, *args, **kwargs):
        # Método para personalizar la lógica de guardado del objeto
        if self.calificado.rol_id == 2:
            # Si el calificado es un conductor, ajustar la categoría utilizando las opciones para conductores
            self.categoria = self.clean_choice(self.categoria, self.CONDUCTOR_CATEGORIA_CHOICES)
        elif self.calificado.rol_id == 1:
            # Si el calificado es un pasajero, ajustar la categoría utilizando las opciones para pasajeros
            self.categoria = self.clean_choice(self.categoria, self.PASAJERO_CATEGORIA_CHOICES)

        # Llamar al método de guardado del modelo base
        super(Calificacion, self).save(*args, **kwargs)

    def clean_choice(self, selected_choice, valid_choices):
        # Método para limpiar la opción seleccionada, utilizando la primera opción válida si no hay coincidencias
        clean_choice = next((choice[0] for choice in valid_choices if choice[0] == selected_choice), None)
        return clean_choice or valid_choices[0][0]