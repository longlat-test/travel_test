from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework.schemas import SchemaGenerator
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.authentication import TokenAuthentication
from rest_framework_swagger import renderers

from .serializers import ProfileSerializers, ProfilePostSerializers, MyProfileSerializers

class ProfileView(APIView):

    permission_classes = [permissions.AllowAny, ]
    def get(self, request):
        profile = Profile.objects.all()
        serializer = ProfileSerializers(profile, many=True)
        return Response({"data": serializer.data})
class MyProfileView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]
    def get(self, request):
        profile = Profile.objects.filter(user=request.user)
        serializer = MyProfileSerializers(profile, many=True)
        return Response({"data": serializer.data})
class DetailsPost(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    def post(self, request, *arg):
        #details = request.data.get("details")
        details = ProfilePostSerializers(data=request.data)
        if details.is_valid():
           details.save(user=request.user)
           return Response(status=201)
        else:
            return Response(status=400)


class SwaggerSchemaView(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)

        return Response(schema)
# Create your views here.
