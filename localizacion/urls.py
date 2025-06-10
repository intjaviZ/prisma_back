# urls.py
from django.urls import path
from .views import EstadoListAPIView, MunicipiosListAPIView, EscuelaListAPIView, GrupoListAPIView

urlpatterns = [
    path('estados/', EstadoListAPIView.as_view(), name='lista-estados'),
    path('municipios/<int:pk>/', MunicipiosListAPIView.as_view(), name='lista-municipios'),
    path('escuelas/', EscuelaListAPIView.as_view(), name='lista-escuelas'),
    path('escuelas/<int:pk>/', EscuelaListAPIView.as_view(), name='lista-escuelas-id'),
    path('grupos/<int:pk>/', GrupoListAPIView.as_view(), name='lista-grupos'),
]
