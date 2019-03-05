from rest_framework import serializers

from .models import Profile, Folowers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer



class ProfileSerializers(serializers.ModelSerializer):

    image = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = Profile
        fields = ('user', 'status', 'location', 'image',  )
class MyProfileSerializers(serializers.ModelSerializer):


    class Meta:
        model = Profile
        fields = ('location', 'status', 'image', 'birthday', )

class ProfilePostSerializers(serializers.ModelSerializer):


    class Meta:
        model = Profile
        fields = ('status', )
class ProfileFotoSerializers(serializers.ModelSerializer):


    class Meta:
        model = Profile
        fields = ('image',)
class ProfileSubscribeSerializers(serializers.ModelSerializer):


    class Meta:
        model = Profile
        fields = ('folowing_id', )
class SnippetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('status', 'location')
