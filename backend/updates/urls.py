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
] 