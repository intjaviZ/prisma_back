from django.urls import path
from .views import DimensionListAPIView, PreguntaListAPIView, EscalasValoracionListAPIView, ResultadosAPIView, EvaluacionListAPIView

urlpatterns = [
    path('dimensiones/', DimensionListAPIView.as_view(), name='lista-dimensiones'),
    path('evaluaciones/', EvaluacionListAPIView.as_view(), name='lista-evaluaciones'),
    path('preguntas/', PreguntaListAPIView.as_view(), name='lista-preguntas'),
    path('opciones/', EscalasValoracionListAPIView.as_view(), name='lista-opciones'),
    path('resultados/', ResultadosAPIView.as_view(), name='resultados'),
    path('resultado/<int:pk>', ResultadosAPIView.as_view(), name='elemento-resultados'),
]