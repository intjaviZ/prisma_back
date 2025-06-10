from django.shortcuts import get_list_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Estado, Municipio, Escuela, Grupo, Alumno
from .serializers import EstadoSerializer, MunicipioSerializer, EscuelaSerializer, GrupoSerializer, AlumnoSerializer


class EstadoListAPIView(APIView):
    @csrf_exempt
    def get(self, request):
        estados = get_list_or_404(Estado, activa=True)
        serializer = EstadoSerializer(estados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MunicipiosListAPIView(APIView):
    @csrf_exempt
    def get(self, request, pk):
        municipios = get_list_or_404(Municipio, estado_id=pk, activa=True)
        serializer = MunicipioSerializer(municipios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EscuelaListAPIView(APIView):
    @csrf_exempt
    def get(self, request):
        escuelas = get_list_or_404(Escuela, activa=True)
        serializer = EscuelaSerializer(escuelas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @csrf_exempt
    def getId(self, request, pk):
        escuelas = get_list_or_404(Escuela, municipio_id=pk, activa=True)
        serializer = EscuelaSerializer(escuelas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GrupoListAPIView(APIView):
    @csrf_exempt
    def get(self, request, pk):
        grupos = get_list_or_404(Grupo, escuela_id=pk)
        serializer = GrupoSerializer(grupos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)