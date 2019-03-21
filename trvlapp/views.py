from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
import requests
import json
import random
import os
from datetime import timedelta, datetime
import struct

import hashlib
from rest_framework.schemas import SchemaGenerator
from django.contrib.auth.models import User
from .models import Profile, Folowers, Event, User, PasswordResetToken
from rest_framework.authentication import TokenAuthentication
from rest_framework_swagger import renderers
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.core.mail import EmailMessage

from django.contrib.auth import get_user_model, login
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from .serializers import ProfileSerializers, ProfilePostSerializers, MyProfileSerializers, ProfileFotoSerializers, ProfileSubscribeSerializers, SnippetSerializer, EventPostSerializers, EventGetSerializers, EventPutSerializers, UserActivateSerializer, AddCommentSerialer, EventBalanceSerializers

class ProfileView(APIView):   #вьешка для получения пользователя по айди

    permission_classes = [permissions.AllowAny, ]

    def get(self, request):
        profile = Profile.objects.filter(user=request.data['user'])
        print(profile)
        print(request.data['user'])
        serializer = ProfileSerializers(profile, many=True)
        print(serializer)
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
        print(profiles)
        folowers = Profile.objects.filter(user__in=profiles)
        print(folowers)
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
        try:
           status = ProfilePostSerializers(data=request.data)
           print(status)
           if status.is_valid():
              status.save(user=request.user)
              return Response("Добавлено")
           else:
              return Response("Не добавлено")
        except:
            return Response("Такой пользователь уже существует")
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

class ListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ] # получения списка пользователей и фильтрация по локации
    serializer_class = ProfileSerializers
    queryset = Profile.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('location', )
class EventCRUD(APIView):  #создание модели Event

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        author = get_object_or_404(Profile, user=request.user)
        profile_currency = author.profile_currency #получение события
        profile = Event.objects.filter(author=author)
        serializer = EventGetSerializers(profile, many=True)
        get_json = requests.get(
             'https://www.cbr-xml-daily.ru/daily_json.js'
        )

        data = get_json.json()
        mylist = []

        profile_valuet = data['Valute'][profile_currency]['Value']
        print(int(serializer.data[0]['balance']))
        profile_valuet = profile_valuet * int(serializer.data[0]['balance'])
        for profile in profile:

            profile.profile_balance = profile_valuet
            profile.save()
        print(profile.profile_balance)
        #mylist.append(str(profile_valuet))
        #mylist = { 'profile_balance' : mylist}
        #serializer1 = EventBalanceSerializers(profile, data=mylist, many=True)
        #print(serializer1)
        #if serializer1.is_valid():
           #serializer1.save()
          # print(serializer1)
        return Response(serializer.data  )

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
class Signup(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        if profile.active == False:
           user = get_object_or_404(User, email=request.user)
           mail_subject = 'Activate your account.'
           current_site = get_current_site(request)
           uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
           token = account_activation_token.make_token(user)
           print(token)
           activation_link = "{0}api/activated/{1}/{2}".format(current_site, uid, token)
           message = "Hello {0},\n {1}".format(user.email, activation_link)
           email = EmailMessage(mail_subject, message, to=[user.email])
           email.send()
           return Response('Please confirm your email address to complete the registration')
        else:
           return Response('Ваш аккаунт уже активирован')

class Activate(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    #User = get_user_model()
    print(User)
    def get(self, request, uidb64, token):
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(id=uid)
        print(user)
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
            print(token)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):

            user = None

        if user is not None and account_activation_token.check_token(user, token):
            profile = get_object_or_404(Profile, user=user)
            print(request.user)
            # activate user and login:
            profile.active = True
            profile.save()
            #user.save()
            #login(request, user)
            return HttpResponse('активация прошла успешно')

        else:
            return HttpResponse('Activation link is invalid!')
class Valuet(APIView):

    permission_classes = [permissions.AllowAny]
    def get(self, request):
        #get_json = requests.get(
             #'https://www.cbr-xml-daily.ru/daily_json.js'
        #)

        #data = get_json.json()
        #print(data['Valute'])
        try:
        # Выполняем запрос к API.
           get_json = requests.get(
                'https://www.cbr-xml-daily.ru/daily_json.js'
           )

           data = get_json.json()
           profile_valuet = data['Valute']['USD']['Value']
           #print(profile_valuet)
           return HttpResponse(profile_valuet)

        except:
           return HttpResponse('данные не получены')


class ForgotPassword(APIView):

    permission_classes = [permissions.AllowAny, ]

    def post(self, request):

        try:
            user = get_object_or_404(User, email=request.data['email'])
            mail_subject = 'Ваш новый временный пароль'

            snippet = PasswordResetToken.objects.get(user=user)
            hash = hashlib.sha1()
            activation_number = str(random.randint(100000, 999999))
            activation_number1 = activation_number.encode('utf-8')
            print(activation_number1)
            #h = hashlib.md5(activation_number1).hexdigest()
            user.set_password(activation_number)
            user.save()

            #print(activation_number)
            message = "Hello {0},\n {1}".format(user.email, activation_number)
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()

            return Response('Please confirm your email address to complete the registration')
        except:
            return Response('нет такого емайла')
class AddComment(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        snippet = AddCommentSerialer(data=request.data)
        if snippet.is_valid():
           snippet.save(authors=request.user)
           #print(serializer.data)
           return Response("добавлено")
        else:
           return Response("Не добавлено")

# class Tags(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated, ] # получения списка тегов
#     serializer_class = ProfileSerializers
#     queryset = Profile.objects.all()
#     filter_backends = (DjangoFilterBackend, )
#     filter_fields = ('location', )


# class ResetPassword(APIView):
#
#     permission_classes = [permissions.AllowAny, ]
#
#     def post(self, request):
#
#         request_number = request.data['number']
#         activation_number1 = request_number.encode('utf-8')
#         h = hashlib.md5(activation_number1).hexdigest()
#         print(h)
#         snippet = PasswordResetToken.objects.get(user=request.data['user'])
#         now = datetime.now()
#         if snippet.hash_id == h and snippet create_data > now:
#
#
#         return Response ('ок')




# Create your views here.
