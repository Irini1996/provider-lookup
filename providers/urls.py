from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'providers', views.ProviderViewSet)
router.register(r'taxonomies', views.TaxonomyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('find/', views.find_provider, name='find_provider'),
]
