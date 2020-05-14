from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from updates import views


urlpatterns = [
    url(r'^$', views.MainPage.as_view())
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)