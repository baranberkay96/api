from django.core.mail import EmailMessage
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework import status, viewsets
from . import models, serializers
from . import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.http import JsonResponse, HttpResponse
import datetime
from django.utils import timezone
import json
from rest_framework.renderers import JSONRenderer
from django.db import connections
from rest_framework_jwt.settings import api_settings
import hashlib
import sys
sys.path.insert(0, 'klplatform/api/kelproject/Utilities')
from Utilities.email import EmailOperations
from urllib.parse import urlparse
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
import sys
from django.forms.models import model_to_dict



def token_generator(request):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(request.user)
    return jwt_encode_handler(payload)


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_user(request):
    es = EmailOperations()
    serialized = serializers.user_profileSerializer(data=request.data)


    if serialized.is_valid():
        user = serialized.save()
        # set_def_interval(request.data["email"])
        #user = models.UserProfile.objects.get(email=request.data["email"])

        token = token_generator(request)

        name = 'Info Mezun Platformu'
        message = 'http://kabataserkek.com.tr/verify-token' + token + "/"
        from_email = request.data['email']
        es.sendEmail('baranberkay96@gmail.com', from_email, name, message)

        user.confirmation_token = token
        user.save()
        return Response(status=status.HTTP_200_OK, data=model_to_dict(user))

    else:
        print(serialized.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=None)

@api_view(['POST'])
@permission_classes((AllowAny,))
def confirm_user_creation(*args, **kwargs):
    token = kwargs.pop('token')
    user = models.UserProfile.objects.get(confirmation_token=token)

    if user.confirmation_token == token:
        user.is_active = True
        user.save()
        return Response(status=status.HTTP_200_OK, data=None)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=None)

@api_view(['POST'])
@permission_classes((AllowAny,))
def send_forget_password_email(request):

    es = EmailOperations()
    email = request.data["email"]
    token = token_generator(request)
    user = models.UserProfile.objects.get(email=email)

    if user is None:
        return Response(status=status.HTTP_404_NOT_FOUND, data=None)
    elif (timezone.now() - user.change_password_request_date).days >= 1 or user.change_password_count < 4:
        user.confirmation_token = token
        user.change_password_request_date = timezone.now()
        user.change_password_count += 1
        user.save()

        name = 'Info Mezun Platformu'

        message = 'http://kabataserkek.com.tr/confirm_mail/' + token + "/"
        from_email = request.data['email']

        es.sendEmail('baranberkay96@datapare.com', from_email, name,
                     '<h4> If you are not the one who changed the password please do not click on the link.''</h4>'
                     + '<h4> Click link to activate your password :' + message + '</h4>'
                     )
        return Response(status=status.HTTP_200_OK, data=None)
    else:
        return Response(status=status.HTTP_200_OK, data=None)

@api_view(['POST'])
@permission_classes((AllowAny,))
def set_new_password(request):

    token = request.data["token"]
    new_password = request.data["new_password"]
    user = models.UserProfile.objects.get(confirmation_token=token)

    if user.confirmation_token == token:
        user.set_password(new_password)
        user.change_password_count = 1
        user.save()
        return Response(status=status.HTTP_200_OK, data=None)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=None)

@api_view(['GET'])
@permission_classes((IsAuthenticated, IsOwnerOrReadOnly,))
def get_user(request, pk, format=None):
    """Handles update, delete and retrive for an instance of user profile"""

    if str(request.user.id) == str(pk):
        try:
            user_profile = models.UserProfile.objects.get(pk=pk)
            return Response(status=status.HTTP_200_OK, data=model_to_dict(user_profile))
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_404_NOT_FOUND, data=None)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=None)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def set_user_password(request):
    user = request.user
    current_password = request.data['current_password']
    new_password = request.data['new_password']

    if user.check_password(current_password):
        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_200_OK, data=None)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=None)
    return Response(json_response, status=json_response["status"])




