from rest_framework import serializers
from .models import Estado, Municipio, Escuela, Grupo, Alumno

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ['id', 'estado'] 

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ['id', 'municipio']

class EscuelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escuela
        fields = ['id', 'escuela']

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ['id', 'grupo']

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ['id', 'alumno', 'num_control', 'escuela', 'grupo']