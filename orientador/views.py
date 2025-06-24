from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, OuterRef, Subquery, F
from .models import PreguntaFrecuente, EntornoVR, Orientador, OrientadorToken
from localizacion.models import Alumno
from test.models import Resultado
from .serializers import PreguntaRespuestaSerializer, EntornoVRSerializer, OrientadorSerializer

from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404

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
                escuela_id=2,
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
    
@api_view(['POST'])
def login(request):
    orientador = get_object_or_404(Orientador,
        nombre=request.data['username'],
        escuela=request.data['escuelaID'],
    )

    if not orientador.check_password(request.data['password']):
        return Response({ "error": "invalid password", "permissions": False }, status=status.HTTP_400_BAD_REQUEST)

    token, _ = OrientadorToken.objects.get_or_create(orientador=orientador)

    serializer = OrientadorSerializer(orientador)
    response = Response({"token": token.key, "usuario": serializer.data}, status=status.HTTP_200_OK)
    response.set_cookie(
        key='token',
        value=token.key,
        httponly=True,
        samesite='None',
        secure=True
    )
    return response

class EstadisticasGeneralesAPIView(APIView):
    def post(self, request):
        escuela_id_data = request.data.get('escuelaId')
        grupo_id_data = request.data.get('grupoId')
        dimension_id_data = request.data.get('dimensionId')
        evaluacion_id_data = request.data.get('evaluacionId')

        # 1. Número total de alumnos
        if escuela_id_data != 0 and grupo_id_data != 0 and dimension_id_data != 0 and evaluacion_id_data != 0:
            print("esta1")
            resultados_recientes = Resultado.objects.filter(alumno=OuterRef('pk')).order_by('-fecha')
            alumnos_filtrados = Alumno.objects.filter(escuela_id=escuela_id_data, grupo_id=grupo_id_data, resultados__isnull=False).annotate(
                evaluacion_id=Subquery(resultados_recientes.values('evaluacion_id')[:1]),
                dimension_id=Subquery(resultados_recientes.values('dimension_id')[:1]),
            )
            total_alumnos = alumnos_filtrados.filter(evaluacion_id=evaluacion_id_data,dimension_id=dimension_id_data).count()
        elif escuela_id_data != 0 and grupo_id_data != 0 and dimension_id_data != 0:
            print("esta2")
            resultados_recientes = Resultado.objects.filter(alumno=OuterRef('pk')).order_by('-fecha')
            alumnos_filtrados = Alumno.objects.filter(escuela_id=escuela_id_data, grupo_id=grupo_id_data, resultados__isnull=False).annotate(
                dimension_id=Subquery(resultados_recientes.values('dimension_id')[:1]),
            )
            total_alumnos = alumnos_filtrados.filter(dimension_id=dimension_id_data).count()
        elif escuela_id_data != 0 and grupo_id_data != 0 and evaluacion_id_data != 0:
            print("esta5")
            resultados_recientes = Resultado.objects.filter(alumno=OuterRef('pk')).order_by('-fecha')
            alumnos_filtrados = Alumno.objects.filter(escuela_id=escuela_id_data, grupo_id=grupo_id_data, resultados__isnull=False).annotate(
                evaluacion_id=Subquery(resultados_recientes.values('evaluacion_id')[:1]),
            )
            total_alumnos = alumnos_filtrados.filter(evaluacion_id=evaluacion_id_data).count()
        elif escuela_id_data != 0 and grupo_id_data != 0:
            print("esta3")
            total_alumnos = Alumno.objects.filter(escuela_id=escuela_id_data, grupo_id=grupo_id_data, resultados__isnull=False).count()
        elif escuela_id_data != 0:
            print("esta4")
            total_alumnos = Alumno.objects.filter(escuela_id=escuela_id_data).count()
        else:
            return Response(
                {"error": "Debes especificar una escuela"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Suma de resultados con evaluación 3 y 4
        
        total_resultados = Resultado.objects.filter(evaluacion_id__in=[3, 4],  alumno__escuela_id=2).count()

        # 3. Dimensión con más resultados asociados
        dimension_frecuente = Resultado.objects.filter(alumno__escuela_id=2).values('dimension__id', 'dimension__dimension') \
            .annotate(total=Count('dimension')) \
            .order_by('-total').first()

        dimension_nombre = dimension_frecuente['dimension__dimension'] if dimension_frecuente else None
        dimension_total = dimension_frecuente['total'] if dimension_frecuente else 0

        # 4. Riesgo con más resultados asociados
        riesgo_frecuente = Resultado.objects.filter(alumno__escuela_id=2).values('riesgo__id', 'riesgo__riesgo') \
            .annotate(total=Count('riesgo')) \
            .order_by('-total').first()

        riesgo_nombre = riesgo_frecuente['riesgo__riesgo'] if riesgo_frecuente else None
        riesgo_total = riesgo_frecuente['total'] if riesgo_frecuente else 0

        # Respuesta JSON
        return Response({
            "total_alumnos": total_alumnos,
            "total_evaluacion": total_resultados,
            "dimension_mas_frecuente": {
                "nombre": dimension_nombre,
                "total": dimension_total
            },
            "riesgo_mas_frecuente": {
                "nombre": riesgo_nombre,
                "total": riesgo_total
            }
        })