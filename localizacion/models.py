from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Estado(models.Model):
    estado = models.CharField(max_length=100)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.estado


class Municipio(models.Model):
    municipio = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='municipios')
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.municipio}, {self.estado}"


class Escuela(models.Model):
    escuela = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='escuelas')
    clave = models.CharField(max_length=30)
    correo = models.EmailField(blank=True, null=True)
    key = models.CharField(max_length=255, blank=True, null=True)
    activa = models.BooleanField(default=True)

    def set_key(self, raw_key):
        """Cifra el API key"""
        self.key = make_password(raw_key)

    def check_key(self, raw_key):
        """Verifica el API key"""
        return check_password(raw_key, self.key)

    def __str__(self):
        return self.escuela


class Grupo(models.Model):
    grupo = models.CharField(max_length=50)
    num_alumnos = models.PositiveIntegerField()
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE, related_name='grupos')

    def __str__(self):
        return f"{self.grupo} ({self.escuela})"


class Alumno(models.Model):
    alumno = models.CharField(max_length=150)
    num_control = models.CharField(max_length=20)
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE, related_name='alumnos')
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='alumnos')

    def __str__(self):
        return f"{self.alumno} ({self.num_control})"
