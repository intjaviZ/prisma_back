from django.urls import path
from .views import PreguntasFrecuentesAPIView, EntornoVRAPIView, EstadisticasGeneralesAPIView
from . import views

urlpatterns = [
    path('login/', views.login ),
    path('preguntasFrec/', PreguntasFrecuentesAPIView.as_view(), name='preguntas_frecuentes'),
    path('entornosVr/', EntornoVRAPIView.as_view(), name='entornos_vr'),
    path('general/', EstadisticasGeneralesAPIView.as_view(), name='stats_generales'),
]
