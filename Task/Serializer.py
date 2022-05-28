# do not mix the capitalization on files; lower-case is best practice -> serializer.py

from django.contrib.auth.models import User
from rest_framework import serializers

from Task.models import Task, Folder

from django.contrib.auth import authenticate

from rest_framework import serializers


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


# The serializer class that should be used for validating and deserializing input, and for serializing output. Typically, you must either set this attribute, or override the get_serializer_class() method
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'Due_date', 'Folder', 'Title', 'Description', 'Responsible_user', 'Repeat_Days', 'Priority',
                  'Completed']
        Depth=1#value of Depth decides how nested values are returned for example if its 1 it shows id and Name of Folder
        #other wise it would have just shown the name .Same goes or User model

class FolderSerializer(
    serializers.ModelSerializer):  # serializers also give a map of how to serialize to JSON and deserialize it back to python datatypes
    class Meta:
        model = Folder
        fields = ['id','Name']


class LoginSerializer(
    serializers.Serializer):  # the idea of serializers it that your taking something that is specifically a python DT, and moving it to something readable by Django auth
    # This serializer defines fields for authentication:
    # It will try to authenticate the user with when validated.
    # https: // www.guguweb.com / 2022 / 01 / 23 / django - rest - framework - authentication - the - easy - way /  make your URLs clickable
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):  # This function is called before create in views because the data needs to be validated
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
