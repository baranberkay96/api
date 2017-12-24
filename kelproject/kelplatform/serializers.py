from rest_framework import serializers
from . import models
import datetime

class user_profileSerializer(serializers.ModelSerializer):
    """A serializer for our user profile object"""


    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name','is_superuser','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new user"""

        user = models.UserProfile(
            email=validated_data['email'],
            name=validated_data['name']

        )

        user.set_password(validated_data['password'])
        user.save()
        return user
