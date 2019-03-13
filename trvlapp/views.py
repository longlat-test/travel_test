from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from rest_framework.schemas import SchemaGenerator
from django.contrib.auth.models import User
from .models import Profile, Folowers, Event, User
from rest_framework.authentication import TokenAuthentication
from rest_framework_swagger import renderers

from .serializers import ProfileSerializers, ProfilePostSerializers, MyProfileSerializers, ProfileFotoSerializers, ProfileSubscribeSerializers, SnippetSerializer, EventPostSerializers, EventGetSerializers, EventPutSerializers

class ProfileView(APIView):   #вьешка для получения пользователя по айди

    permission_classes = [permissions.AllowAny, ]

    def get(self, request):
        profile = Profile.objects.filter(user=request.data['user'])
        print(profile)
        print(request.data['user'])
        serializer = ProfileSerializers(profile, many=True)
        return Response(serializer.data)

class MyProfileView(APIView): #вьюшка для получения текущего пользователя

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        profile = Profile.objects.filter(user=request.user)
        serializer = MyProfileSerializers(profile, many=True)
        return Response(serializer.data[0])
class GetSubscribe(APIView):  #вью подписчиков/подписок

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):   #получение подписок
        profiles = Folowers.objects.filter(users_id=request.user).values('folowing_id')
        folowers = Profile.objects.filter(user__in=profiles)
        serializer = ProfileSerializers(folowers, many=True)
        return JsonResponse(serializer.data, safe=False)

    def put(self, request, *arg):  #добавление подписок
        snippet = Folowers.objects.get(users_id=request.user)
        serializer = ProfileSubscribeSerializers(snippet, data=request.data)
        if serializer.is_valid():
           snippet.folowing_id.add(request.data['folowing_id'])
           print(serializer.data)
           return Response("добавлено")
        else:
           return Response("Не добавлено")
class DetailsPost(APIView):  #создание модели Profile

    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *arg):
        #details = request.data.get("details")
        status = ProfilePostSerializers(data=request.data)
        if status.is_valid():
           status.save(user=request.user)
           return Response("Добавлено")
        else:
            return Response("Не добавлено")
class UpdateProfile(APIView): #вьюшка обновления данных пользователя

    permission_classes = [permissions.IsAuthenticated, ]

    def put(self, request, *arg):
        snippet = get_object_or_404(Profile, user=request.user)
        serializer = SnippetSerializer(snippet, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)



class ApiFoto(APIView): #вьюшка изображения
    permission_classes = [permissions.IsAuthenticated, ]
    def post(self, request, *arg): #добавление изображения
        print (request.data)
        snippet = get_object_or_404(Profile, user=request.user)
        foto = ProfileFotoSerializers(snippet, data=request.data)
        if foto.is_valid():
           foto.save()
           return Response("добавлено")
        else:
            return Response("не добавлено")
    def get(self, request): #получение изображения
        profile = Profile.objects.filter(user=request.user)
        serializer = ProfileFotoSerializers(profile, many=True)
        return Response(serializer.data)

class ListView(generics.ListAPIView): # получения списка пользователей
    serializer_class = ProfileSerializers
    queryset = Profile.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('location', )
class EventCRUD(APIView):  #создание модели Event

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        author = get_object_or_404(Profile, user=request.user) #получение события
        profile = Event.objects.filter(author=author)
        serializer = EventGetSerializers(profile, many=True)
        return Response(serializer.data)

    def post(self, request, *arg):
        status = EventPostSerializers(data=request.data)

        print(request.data)
        if status.is_valid():
           author = get_object_or_404(Profile, user=request.user)
           status.save(author=author)
           return Response("Добавлено")
        else:
            return Response("Не добавлено")
    def put(self, request, *arg):
        author = get_object_or_404(Profile, user=request.user)
        snippet = get_object_or_404(Event, author=author, event_id=request.data['event_id'])
        print(snippet)
        serializer = EventPutSerializers(snippet, data=request.data)
        #print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response('не добавлено')

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
