from rest_framework import serializers

from .models import Profile


class ProfileSerializers(serializers.ModelSerializer):


    class Meta:
        model = Profile
        fields = ('user', 'details' )
class MyProfileSerializers(serializers.ModelSerializer):


    class Meta:
        model = Profile
        fields = ('details', )

class ProfilePostSerializers(serializers.ModelSerializer):


    class Meta:
        model = Profile
        fields = ('details', )
