from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from updates import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'new_cases', views.RecordViewSet)

urlpatterns = [
    path('', views.MainPage.as_view()),
    path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)