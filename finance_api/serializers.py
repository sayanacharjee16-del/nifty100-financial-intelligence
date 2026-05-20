from rest_framework import serializers
from finance_api.models import DimCompany, FactMlScores

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = DimCompany
        fields = '__all__'

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactMlScores
        fields = '__all__'