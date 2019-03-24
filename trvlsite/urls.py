"""trvlsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger import renderers
from rest_framework.schemas import get_schema_view

#class JSONOpenAPIRenderer(renderers.OpenAPIRenderer):
#    media_type = 'application/vdn.name.v1+json'


schema_view = get_swagger_view(title='Longlat Travel')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("trvlapp.urls")),
    path('', schema_view),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
#    path('auth/', include('djoser.urls.jwt')),
    path('docs/', include_docs_urls(title='My API title'))

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
