from rest_framework import serializers
from .models import PreguntaFrecuente, Orientador

class PreguntaRespuestaSerializer(serializers.ModelSerializer):
    idPregunta = serializers.IntegerField(source='id')
    pregunta = serializers.CharField(source='pregunta_frec')
    respuesta = serializers.CharField(source='respuesta_frec.respuesta')

    class Meta:
        model = PreguntaFrecuente
        fields = ['idPregunta', 'pregunta', 'respuesta']

class EntornoVRSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField(max_length=120, default="Video de apoyo", allow_blank=True)
    descripcion = serializers.CharField(allow_blank=True, required=False)
    video = serializers.URLField(max_length=300)

    class Meta:
        fields = ['id', 'nombre', 'descripcion', 'video']

class OrientadorSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField()
    escuelaId = serializers.IntegerField(source='escuela_id')
    permissions = serializers.BooleanField(default=True)

    class Meta:
        model = Orientador
        fields = ['nombre', 'escuelaId', 'permissions']