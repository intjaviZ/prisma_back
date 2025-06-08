from rest_framework import serializers
from .models import Dimension, Pregunta, EscalaValoracion, Resultado

class DimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = ['id', 'dimension']

class PreguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = ['id', 'pregunta', 'dimension']

class EscalasValoracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscalaValoracion
        fields = ['id', 'escala', 'valor', 'dimension']

class EscuelaSerializer(serializers.Serializer):
    estado = serializers.IntegerField()
    escuela = serializers.IntegerField()
    ciudad = serializers.IntegerField()
    grupo = serializers.IntegerField()

class AlumnoSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=150)
    numero_control = serializers.CharField(max_length=20)

class RespuestaSerializer(serializers.DictField):
    child = serializers.IntegerField()

class ResultadoEntradaSerializer(serializers.Serializer):
    escuela = EscuelaSerializer()
    alumno = AlumnoSerializer()
    respuestas = RespuestaSerializer()
    comentario = serializers.CharField(max_length=150, required=False)

class ResultadoRespuestaSerializer(serializers.Serializer):
    idEscuela = serializers.IntegerField()
    idEvaluacion = serializers.IntegerField()
    idDimension = serializers.IntegerField()
    idRiesgo = serializers.IntegerField()
    evaluacionGeneral = serializers.CharField(max_length=100)
    evaluacionDimension = serializers.CharField(max_length=100)
    dimension = serializers.CharField(max_length=100)
    riesgo = serializers.CharField(max_length=100)