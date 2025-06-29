from rest_framework import serializers
from .models import TokenComplianceProfile, HolderAnalysisResult

class TokenComplianceProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenComplianceProfile
        fields = '__all__'

class HolderAnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = HolderAnalysisResult
        fields = '__all__'