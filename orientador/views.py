from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PreguntaFrecuente, EntornoVR
from .serializers import PreguntaRespuestaSerializer, EntornoVRSerializer

class PreguntasFrecuentesAPIView (APIView):
    def post(self, request):
        id_escuela = request.data.get('idEscuela')
        id_dimension = request.data.get('idDimension')
        id_riesgo = request.data.get('idRiesgo')

        if not id_escuela and not id_dimension:
            return Response(
                {"error": "No podemos mostrarte preguntas sin conocer tu información de la fase 1."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if id_riesgo:
            preguntas = PreguntaFrecuente.objects.filter(
                escuela_id=id_escuela,
                dimension_id=id_dimension,
                riesgo_id=id_riesgo,
                activa=True
            ).select_related('respuesta_frec')
        if id_escuela:
            preguntas = PreguntaFrecuente.objects.filter(
                escuela_id=id_escuela,
                activa=True
            ).select_related('respuesta_frec')
        if id_dimension:
            preguntas = PreguntaFrecuente.objects.filter(
                escuela_id=1,
                dimension_id=id_dimension,
                activa=True
            ).select_related('respuesta_frec')

        serializer = PreguntaRespuestaSerializer(preguntas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class EntornoVRAPIView(APIView):
    def post(self, request):
        id_escuela = request.data.get('idEscuela')
        id_dimension = request.data.get('idDimension')
        id_riesgo = request.data.get('idRiesgo')

        if not id_escuela and not id_dimension:
            return Response(
                {"error": "No podemos mostrarte preguntas sin conocer tu información de la fase 1."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if id_riesgo:
            entornos = EntornoVR.objects.filter(
                escuela_id=id_escuela,
                dimension_id=id_dimension,
                riesgo_id=id_riesgo,
                activa=True
            ).select_related('escuela', 'dimension', 'riesgo')
        if not id_dimension:
            entornos = EntornoVR.objects.filter(
                escuela_id=id_escuela,
                activa=True
            ).select_related('escuela')
        else:
            entornos = EntornoVR.objects.filter(
                dimension_id=id_dimension,
                activa=True
            ).select_related('dimension')

        serializer = EntornoVRSerializer(entornos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)