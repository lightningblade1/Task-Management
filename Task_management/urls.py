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
    path('log-out/', LogoutView.as_view(), name='log_out'),  # call it "logout"
    url('CreateTask', CreateTask.as_view()),  # keep your URLs lower-case -> create-task; even better stick with REST convention -> make sure to check the quickstart of DRF: https://www.django-rest-framework.org/tutorial/quickstart/#quickstart

]
