from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from localizacion.models import Alumno
from .models import Dimension, Pregunta, EscalaValoracion, Resultado, Evaluacion, Riesgo
from .serializers import DimensionSerializer, PreguntaSerializer, EscalasValoracionSerializer, ResultadoEntradaSerializer, ResultadoRespuestaSerializer

class DimensionListAPIView(APIView):
    @csrf_exempt
    def get(self, request):
        dimension = get_list_or_404(Dimension)
        serializer = DimensionSerializer(dimension, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PreguntaListAPIView(APIView):
    @csrf_exempt
    def get(self, request):
        pregunta = get_list_or_404(Pregunta)
        serializer = PreguntaSerializer(pregunta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EscalasValoracionListAPIView(APIView):
    @csrf_exempt
    def get(self, request):
        escalas = get_list_or_404(EscalaValoracion)
        serializer = EscalasValoracionSerializer(escalas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ResultadosAPIView(APIView):
    def get(self, request, pk):
        resultado = get_object_or_404(Resultado, id=pk)
        alumno = Alumno.objects.filter(id=resultado.alumno_id).first()
        evaluacion = Evaluacion.objects.filter(id=resultado.evaluacion_id).first()
        dimension = Dimension.objects.filter(id=resultado.dimension_id).first()
        riesgo = Riesgo.objects.filter(id=resultado.riesgo_id).first()
        evaluacion_dimension = Evaluacion.objects.filter(id=resultado.eval_dimension_id).first()

        respuesta = {
            "idEscuela": alumno.escuela_id if alumno else None,
            "idEvaluacion": evaluacion.id if evaluacion else None,
            "idDimension": dimension.id if dimension else None,
            "idRiesgo": riesgo.id if riesgo else None,
            "evaluacionGeneral": evaluacion.evaluacion if evaluacion else None,
            "evaluacionDimension": evaluacion_dimension.evaluacion if evaluacion_dimension else None,
            "dimension": dimension.dimension,
            "riesgo": riesgo.riesgo if riesgo else None
        }

        serializer = ResultadoRespuestaSerializer(respuesta)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @csrf_exempt
    def post(self, request):
        serializer = ResultadoEntradaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Extraer datos
        escuela_data = data["escuela"]
        alumno_data = data["alumno"]
        comentario = data.get("comentario", "")
        respuestas_data = data["respuestas"]

        estado_id = escuela_data["estado"]
        escuela_id = escuela_data["escuela"]
        ciudad_id = escuela_data["ciudad"]  # podrías usarlo más adelante
        grupo_id = escuela_data["grupo"]

        num_control = alumno_data["numero_control"]
        nombre = alumno_data["nombre"]

        try:
            with transaction.atomic():
                # Buscar o crear al alumno
                alumno, creado = Alumno.objects.get_or_create(
                    num_control=num_control,
                    defaults={
                        "alumno": nombre,
                        "escuela_id": escuela_id,
                        "grupo_id": grupo_id,
                    }
                )

                dimensiones = {int(k): int(v) for k, v in respuestas_data.items()}
                

                total = sum(dimensiones.values())  # suma total
                maximo_total = 90
                porcentaje_total = round((total / maximo_total) * 100)

                # Evaluación (basado en % total)
                evaluacion = Evaluacion.objects.filter(
                    min_val__lte=porcentaje_total,
                    max_val__gte=porcentaje_total
                ).first()

                dimension_id_peor = min(dimensiones, key=dimensiones.get)
                valor_peor = dimensiones[dimension_id_peor]
                porcentaje_dimension = round((valor_peor / 30) * 100)

                evaluacion_dimension = Evaluacion.objects.filter(
                    min_val__lte=porcentaje_dimension,
                    max_val__gte=porcentaje_dimension
                ).first()

                # Obtener dimension
                dimension = Dimension.objects.filter(id=dimension_id_peor).first()

                riesgo = None
                if porcentaje_dimension < 50:
                    riesgo = Riesgo.objects.filter(dimension_id=dimension_id_peor).first()

                # Guardar resultado
                resultado = Resultado.objects.create(
                    alumno=alumno,
                    evaluacion=evaluacion,
                    riesgo=riesgo,
                    dimension=dimension,
                    resultados=dimensiones,
                    eval_dimension=evaluacion_dimension,
                    comentario=comentario
                )

                respuesta_data = {
                    "idEscuela": alumno.escuela_id if alumno else None,
                    "idEvaluacion": evaluacion.id if evaluacion else None,
                    "idDimension": dimension.id if dimension else None,
                    "idRiesgo": riesgo.id if riesgo else None,
                    "evaluacionGeneral": evaluacion.evaluacion if evaluacion else None,
                    "evaluacionDimension": evaluacion_dimension.evaluacion if evaluacion_dimension else None,
                    "dimension": dimension.dimension,
                    "riesgo": riesgo.riesgo if riesgo else None
                }


            # Serializamos para asegurarnos de que el formato sea válido
            serializer_respuesta = ResultadoRespuestaSerializer(respuesta_data)
            return Response(serializer_respuesta.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)