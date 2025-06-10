from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from localizacion.models import Escuela
from test.models import Dimension, Riesgo
from django.db import models
import secrets

class Orientador(models.Model):
    nombre = models.CharField(max_length=120)
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE, related_name='orientadores')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Hasheada

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.nombre} ({self.escuela})"
    
class OrientadorToken(models.Model):
    orientador = models.OneToOneField(Orientador, on_delete=models.CASCADE, related_name='token')
    key = models.CharField(max_length=40, primary_key=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(20)
        return super().save(*args, **kwargs)


class RespuestaFrecuente(models.Model):
    respuesta = models.CharField(max_length=100)

    def __str__(self):
        return self.respuesta


class PreguntaFrecuente(models.Model):
    pregunta_frec = models.CharField(max_length=100)
    respuesta_frec = models.ForeignKey(RespuestaFrecuente, on_delete=models.SET_NULL, null=True, related_name='preguntas')
    dimension = models.ForeignKey(Dimension, on_delete=models.SET_NULL, null=True, related_name='preguntas_frecuentes')
    riesgo = models.ForeignKey(Riesgo, on_delete=models.SET_NULL, null=True, related_name='preguntas_frecuentes')
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE, related_name='preguntas_frecuentes')
    activa = models.BooleanField(default=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pregunta_frec} ({self.escuela})"


class EntornoVR(models.Model):
    nombre = models.CharField(max_length=120, default="Video de apoyo", null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    video = models.URLField(max_length=300)
    dimension = models.ForeignKey(Dimension, on_delete=models.SET_NULL, null=True, related_name='videos_vr')
    riesgo = models.ForeignKey(Riesgo, on_delete=models.SET_NULL, null=True, related_name='videos_vr')
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE, related_name='videos_vr')
    activa = models.BooleanField(default=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"VR: {self.video} - {self.escuela}"