from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils.contract import fetch_token_metadata

class TokenMetadataView(APIView):
    def get(self, request, address):
        try:
            data = fetch_token_metadata(address)
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=400)