from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from anthropic import Anthropic
from django.conf import settings
from requests import post, exceptions
from decouple import config

class EmotionalSupportView(APIView):
    def post(self, request):
        API_URL = config('API_URL')
        API_TOKEN = settings.API_TOKEN

        input_text = request.data.get("prompt", "")

        if not input_text:
            return Response(
            {"mensaje": "No se ha enviado una pregunta."},
            status=status.HTTP_400_BAD_REQUEST
            )
        
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        payload = {
            "inputs": input_text,
            "parameters": {
                "temperature": 0.4,
                "top_p": 0.8,
                "max_new_tokens": 300
            }
        }

        try:
            response = post(API_URL, headers=headers, json=payload,timeout=90)
            if response.status_code == 200:
                output = response.json()

                if output and isinstance(output, list) and "generated_text" in output[0]:
                    generated_text = output[0]["generated_text"]
                    cleaned_response = generated_text.replace(input_text, "").strip()

                    cleaned_response = cleaned_response.replace("\n", " ").strip()

                    return Response(
                        {"mensaje": cleaned_response},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"mensaje": "Formato inesperado en la respuesta del modelo."},
                        status=status.HTTP_502_BAD_GATEWAY
                    )
            else:
                return Response({
                    "mensaje": "Error al procesar la solicitud",
                    "status_code": response.status_code,
                    "response_text": response.text
                }, status=response.status_code)
        except exceptions.Timeout:
            return Response(
                {"mensaje": "La solicitud al modelo ha superado el tiempo límite."},
                status=status.HTTP_504_GATEWAY_TIMEOUT
            )

        except exceptions.RequestException as e:
            return Response(
                {"mensaje": "Error al conectar con el modelo.", "detalle": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except Exception as e:
            return Response(
                {"mensaje": "Ocurrió un error inesperado.", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class Chat_gpt(APIView):
    def post(self, request):
        user_message = request.data.get("prompt", "")
        try:
            client = OpenAI(
                api_key=settings.API_KEY
            )
            completion = client.chat.completions.create(
              model="gpt-4o-mini",
                store=True,
                messages=[
                    {"role": "user", "content": user_message}
                ])
            response = completion.choices[0].message
            return Response({"respuesta": response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Ocurrió un error al procesar la solicitud: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ClaudeAPIView(APIView):
    def post(self, request):
        # Validar datos de entrada
        prompt = request.data.get('prompt', '')
        if not prompt:
            return Response({'error': 'Prompt requerido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = Anthropic(api_key=settings.API_CLAUDE)
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=300,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return Response({
                'response': response.content[0].text
            }, status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)