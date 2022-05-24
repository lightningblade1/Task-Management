from dateutil.parser import parser
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from Task.Serializer import TaskSerializer, FolderSerializer, LoginSerializer, UserSerializer
from Task.models import Task, Folder


class LoginView(viewsets.ModelViewSet):
    serializer_class = LoginSerializer

    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        print(self.request.GET)
        tasks = User.objects.none()
        return tasks

    def create(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        serializer = UserSerializer(user)

        return Response(serializer.data)


@method_decorator(csrf_exempt, name='post')
class CreateTask(APIView):
    serializer_class = TaskSerializer  # This gives the serializer class that will be used deserialize input think of it as a form class

    def get_queryset(self):
        if self.request.user.is_authenticated:
            tasks = Task.objects.all()

            return tasks
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and 'id' in request.query_params:
            params = kwargs
            id = request.query_params["id"]
            if id != None:
                folder_query = Task.objects.get(id=id)
                serializer = TaskSerializer(folder_query)
                return Response(serializer.data)
        else:
            folder_query = TaskSerializer(self.get_queryset(),
                                          many=True)  # if we dont serialize django gives error that the object cant be serialized so its important to serailize when returning django objects
            # in the above statement many=True because we are returning a query set with many objects.If this is not done django would be expecting only one object to be returned and serialized
            return Response(folder_query.data, status=HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        print(request.user.is_superuser)
        if request.user.is_superuser:

            task_data = request.data
            if task_data["Title"] and task_data["Due_date"] and task_data["Description"] and task_data[
                'Repeat_Days'] != None:
                if 'Completed' not in task_data or task_data["Completed"] == False:
                    new_task = Task.objects.create(Title=task_data["Title"],
                                                   Folder=Folder.objects.get(id=task_data["Folder"]),
                                                   Due_date=task_data["Due_date"],
                                                   Description=task_data["Description"], Priority=task_data["Priority"],
                                                   Completed=False, Repeat_Days=task_data['Repeat_Days'])

                elif task_data["Completed"] == True or task_data["Completed"] == 'true':#you can leave it without true
                    new_task = Task.objects.create(Title=task_data["Title"],
                                                   Folder=Folder.objects.get(id=task_data["Folder"]),
                                                   Due_date=task_data["Due_date"],
                                                   Description=task_data["Description"], Priority=task_data["Priority"],
                                                   Completed=True,
                                                   Repeat_Days=task_data['Repeat_Days'])
                if 'Responsible_user' in task_data:
                    for user in task_data["Responsible_user"]:
                        user_obj = User.objects.get(id=int(user))
                        new_task.Responsible_user.add(user_obj)
                new_task.save()

                serializer = TaskSerializer(new_task)

                return Response(serializer.data)
            else:
                return Response(status=HTTP_400_BAD_REQUEST)
        return Response(status=HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        if request.user.is_superuser and 'id' in request.query_params:
            id = request.query_params["id"]
            Tobject = Task.objects.get(id=id)

            data = request.data

            Tobject.Title = data["Title"]
            Tobject.Folder = Folder.objects.get(id=data["Folder"])
            Tobject.Due_date = data["Due_date"]
            Tobject.Description = data["Description"]
            Tobject.Priority = data["Priority"]
            Tobject.Repeat_Days = data["Repeat_Days"]
            if 'Completed' not in data:
                Tobject.Completed = False
            else:
                Tobject.Completed = data["Completed"]
            Tobject.save()
            serializer = TaskSerializer(Tobject)
            return Response(serializer.data)
        else:
            statuscode = HTTP_401_UNAUTHORIZED
            return Response(status=statuscode)


class CreateFolder(APIView):
    serializer_class = FolderSerializer

    # The generic functions below are convinient because they create frontend elements by default in REST framework API
    def get_queryset(self):
        if self.request.user.is_authenticated:
            cars = Folder.objects.all()
            return cars
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                id = request.query_params["id"]
                if id != None:
                    folder_query = Folder.objects.get(id=id)
                    serializer = FolderSerializer(folder_query)
            except:
                folder_query = self.get_queryset()
                serializer = FolderSerializer(folder_query, many=True)

            return Response(serializer.data)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            new_folder = Folder.objects.create(Name=request.data['Name'])

            new_folder.save()

            serializer = FolderSerializer(new_folder)

            return Response(serializer.data)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):

        if request.query_params["id"] != None and request.user.is_superuser:
            id = request.query_params["id"]
            folder_query = Folder.objects.get(id=id)
            folder_query.delete()
            statuscode = HTTP_200_OK
        else:
            statuscode = HTTP_401_UNAUTHORIZED
        folder_query = self.get_queryset()
        serializer = FolderSerializer(folder_query, many=True)

        return Response(serializer.data, status=statuscode)

    def put(self, request, *args, **kwargs):
        if request.user.is_superuser:
            id = request.query_params["id"]
            Fobject = Folder.objects.get(id=id)

            data = request.data

            Fobject.Name = data["Name"]

            Fobject.save()

            serializer = FolderSerializer(Fobject)
            return Response(serializer.data)
        else:
            statuscode = HTTP_401_UNAUTHORIZED
            return Response(status=statuscode)


class LogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'rest_framework/api.html'
