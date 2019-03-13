from rest_framework import serializers

from .models import Profile, Folowers, Event, User
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer



class ProfileSerializers(serializers.ModelSerializer):

    image = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = Profile
        fields = ( 'user', 'full_name', 'sex', 'status', 'location', 'image', 'background')
class MyProfileSerializers(serializers.ModelSerializer):


    class Meta:
        model = Profile
        fields = ('user', 'full_name', 'sex', 'status', 'location', 'image', 'background', 'age')

class ProfilePostSerializers(serializers.ModelSerializer):


    class Meta:
        model = Profile
        fields = ('status', )
class ProfileFotoSerializers(serializers.ModelSerializer):


    class Meta:
        model = Profile
        fields = ('image',)
class ProfileSubscribersSerializers(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user', )
class ProfileSubscribeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Folowers
        fields = ('folowing_id', )
class SnippetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('status', 'location')
class EventPostSerializers(serializers.ModelSerializer):


    class Meta:
        model = Event
        fields = ('name', 'budget' )
class EventGetSerializers(serializers.ModelSerializer):


    class Meta:
        model = Event
        fields = ('author', 'name', 'budget', 'image', 'location', 'date', 'event_id' )
class EventPutSerializers(serializers.ModelSerializer):


    class Meta:
        model = Event
        fields = ('name', 'budget', 'event_id' )
