from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework.schemas import SchemaGenerator
from django.contrib.auth.models import User
from .models import Profile, Folowers
from rest_framework.authentication import TokenAuthentication
from rest_framework_swagger import renderers

from .serializers import ProfileSerializers, ProfilePostSerializers, MyProfileSerializers, ProfileFotoSerializers, ProfileSubscribeSerializers, SnippetSerializer

class ProfileView(APIView):

    permission_classes = [permissions.AllowAny, ]
    def get(self, request):
        print (request.data)
        profile = Profile.objects.filter(user=request.data['user'])

        serializer = ProfileSerializers(profile, many=True)
        return Response({"data": serializer.data})

class MyProfileView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]
    def get(self, request):
        profile = Profile.objects.filter(user=request.user)
        serializer = MyProfileSerializers(profile, many=True)
        return Response({"data": serializer.data})
class GetSubscribe(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        favorites = ''
        profiles = Profile.objects.filter(folowing_id=request.user)
        #print (profiles)
        profile = Profile.objects.filter(user=request.user)
        print (profile)
        serializer = ProfileSubscribeSerializers(profile, many=True)
        folowers = serializer.data[0]
        print(folowers)
        folowers = folowers['folowing_id']
        print(folowers)
        #folow = Profile.objects.filter(user=folowers)
        for i in folowers:
            folowers_list = []
            folow = Profile.objects.filter(user=i)
            serializer = ProfileSerializers(folow, many=True)
            #print(serializer)

            folowers_list.append(serializer)
            print (folowers_list)

            #folow.append(i)
        #folowers_list = folowers_list[0:]
        #print(folowers_list)
        return Response({"data": serializer.data})
class DetailsPost(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    def post(self, request, *arg):
        #details = request.data.get("details")
        status = ProfilePostSerializers(data=request.data)
        print(status)
        print(request.user.id)
        if status.is_valid():
           status.save(user=request.user)
           return Response("Добавлено")
        else:
            return Response("Не добавлено")
class UpdateProfile(APIView):

    permission_classes = [permissions.IsAuthenticated, ]
    def put(self, request, *arg):
        snippet = get_object_or_404(Profile, user=request.user)
        serializer = SnippetSerializer(snippet, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)



class ApiFoto(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    def post(self, request, *arg):
        print (request.data)
        snippet = get_object_or_404(Profile, user=request.user)
        foto = ProfileFotoSerializers(snippet, data=request.data)
        if foto.is_valid():
           foto.save()
           return Response("добавлено")
        else:
            return Response("не добавлено")
    def get(self, request):
        profile = Profile.objects.filter(user=request.user)
        serializer = ProfileFotoSerializers(profile, many=True)
        return Response({"data": serializer.data})



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
