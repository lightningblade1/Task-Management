from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Task.views import CreateTask, CreateFolder, LoginView, LogoutView

router = DefaultRouter()
router.register('Login', LoginView, basename='Login')




urlpatterns = [
    url('', include(router.urls)),
    path('admin/', admin.site.urls),
    #path('login/', LoginView.as_view()),
    url('CreateFolder', CreateFolder.as_view()),
    path('log-out/', LogoutView.as_view(), name='log_out'),
    url('CreateTask', CreateTask.as_view()),

]
