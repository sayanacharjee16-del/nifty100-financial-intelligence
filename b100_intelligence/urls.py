from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Cleaned up imports: Removed duplicates and fixed the Score name
from finance_api.views import CompanyViewSet, ScoreViewSet, dashboard_home
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
# Ensure this matches 'ScoreViewSet' which we standardized in views.py
router.register(r'scores', ScoreViewSet, basename='score')

urlpatterns = [
    path('', dashboard_home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]