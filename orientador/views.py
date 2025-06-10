from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PreguntaFrecuente, EntornoVR, Orientador
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
    
@api_view(['POST'])
def login(request):
    orientador = get_object_or_404(Orientador,
        username=request.data['username'],
        escuela=request.data['escuelaId'],
        password=request.data['password']
    )
    if not orientador.check_password(request.data['password']):
        return Response({ "error": "invalid password", "permissions": False }, status=status.HTTP_400_BAD_REQUEST)
    
    token, create = Token.objects.get_or_create(user=orientador)
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

# @api_view(['POST'])
# def login(request):
#     user = get_object_or_404(
#         Orientador,
#         nombre=request.data['username'],
#         email=request.data['email'],email=request.data['email'],
#         escuela=request.data['escuelaId']        
#     )
#     if not user.check_password(request.data['password']):
#         return Response({ "error": "invalid password" }, status=status.HTTP_400_BAD_REQUEST)
    
#     token, create = Token.objects.get_or_create(user=user)
    # serializer = User_serializer(instance=user)
    # return Response({"token": token.key, "usuario": serializer.data}, status=status.HTTP_200_OK)

