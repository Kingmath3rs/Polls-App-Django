from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *

from user.serializers import UserSerializer


class CreateAndList(APIView):
    def get(self, request):
        context = {}
        users = User.objects.all()
        context['users'] = UserSerializer(users, many=True).data
        return Response(context, status=HTTP_200_OK)

    def post(self, request):
        context = {}
        user = User(
            username=request.data.get('username'),
            password=make_password(request.data.get('password)')),
        )
        user.save()
        context['user'] = UserSerializer(user).data
        return Response(context, status=HTTP_200_OK)


class UserSingle(APIView):
    def get(self, request, pk):
        context = {}
        try:
            user = User.objects.get(id=pk)
            context['user'] = UserSerializer(user).data
            status_code = HTTP_200_OK
        except:
            context['msg'] = "user bilaakh"
            status_code = HTTP_404_NOT_FOUND
        return Response(context, status=status_code)

    def put(self, request, pk):
        context = {}
        try:
            user = User.objects.get(id=pk)
            user.username = request.data.get('username', user.username)
            if request.data.get('password'):
                user.password = make_password(request.data.get('password'))
            user.save()
            context['user'] = UserSerializer(user).data
            status_code = HTTP_200_OK
        except:
            context['msg'] = "User bilaakh"
            status_code = HTTP_404_NOT_FOUND
        return Response(context, status=status_code)

    def delete(self, request, pk):
        context = {}
        try:
            user = User.objects.get(id=pk)
            user.delete()
            context['msg'] = "User siiiiktir"
            status_code = HTTP_200_OK
        except:
            context['msg'] = "User bilaakh"
            status_code = HTTP_404_NOT_FOUND
        return Response(context, status=status_code)
