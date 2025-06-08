from django.db import models
from localizacion.models import Alumno


class Dimension(models.Model):
    dimension = models.CharField(max_length=40)

    def __str__(self):
        return self.dimension


class Pregunta(models.Model):
    pregunta = models.CharField(max_length=100)
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name='preguntas')

    def __str__(self):
        return self.pregunta


class EscalaValoracion(models.Model):
    escala = models.CharField(max_length=30)
    valor = models.IntegerField()
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name='escalas')

    def __str__(self):
        return f"{self.escala} ({self.valor}) - {self.dimension}"


class Riesgo(models.Model):
    riesgo = models.CharField(max_length=30)
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name='riesgos')

    def __str__(self):
        return f"{self.riesgo} - {self.dimension}"


class Evaluacion(models.Model):
    evaluacion = models.CharField(max_length=50)
    min_val = models.IntegerField()
    max_val = models.IntegerField()

    def __str__(self):
        return f"{self.evaluacion} ({self.min_val} - {self.max_val})"


class Resultado(models.Model):
    resultados = models.JSONField()
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='resultados')
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.SET_NULL, null=True, related_name='resultados')
    riesgo = models.ForeignKey(Riesgo, on_delete=models.SET_NULL, null=True, related_name='resultados')
    dimension = models.ForeignKey(Dimension, on_delete=models.SET_NULL, null=True, related_name='resultados')
    eval_dimension = models.ForeignKey(Evaluacion, on_delete=models.SET_NULL, null=True, related_name='evaluacion_dimension')
    comentario = models.CharField(max_length=150, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resultado de {self.alumno} - {self.dimension} en {self.fecha.date()}"