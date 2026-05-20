from rest_framework import viewsets
from finance_api.models import DimCompany, FactMlScores
from finance_api.serializers import CompanySerializer, ScoreSerializer 
from django.shortcuts import render

def dashboard_home(request):
    return render(request, 'dashboard.html')

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = DimCompany.objects.all()
    serializer_class = CompanySerializer

# Change 'HealthScoreViewSet' to 'ScoreViewSet'
class ScoreViewSet(viewsets.ModelViewSet):
    queryset = FactMlScores.objects.all()
    serializer_class = ScoreSerializer # Use ScoreSerializer here