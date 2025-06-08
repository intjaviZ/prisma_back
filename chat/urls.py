from django.urls import path
from .views import Chat_gpt, EmotionalSupportView, ClaudeAPIView

urlpatterns = [
    path('hugging/', EmotionalSupportView.as_view(), name='hugging'),
    path('openai/', Chat_gpt.as_view(), name='gpt'),
    path('claude/', ClaudeAPIView.as_view(), name='claude-api'),
]