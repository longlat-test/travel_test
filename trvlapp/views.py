from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from django.contrib.auth.models import User
from .models import Profile

from .serializers import ProfileSerializers, ProfilePostSerializers

class ProfileView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]
    def get(self, request):
        profile = Profile.objects.all()
        serializer = ProfileSerializers(profile, many=True)
        return Response({"data": serializer.data})
    def post(self, request):
        details = ProfilePostSerializers(data=request.data)
        if details.is_valid():
            details.save(user=request.user)
            return Response(status=201)
        else:
            return Response(status=400)



# Create your views here.
