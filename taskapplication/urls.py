"""taskapplication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from task.views import IndexView,LoginView1,AddTaskView,TaskListView,TaskDetailView,TaskDeleteView,RegistrationView,LoginView,signout_view,TaskUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/",IndexView.as_view()),
    path("login/",LoginView1.as_view()),
    path("todos/add",AddTaskView.as_view(),name="todo-add"),
    path("todos/all",TaskListView.as_view(),name="todo-all"),
    path("todos/<int:id>",TaskDetailView.as_view(),name="todo-detail"),
    path("todos/<int:id>/remove",TaskDeleteView.as_view(),name="todo-delete"),
    path("accounts/register/",RegistrationView.as_view(),name='register'),
    path('',LoginView.as_view(),name="signin"),
    path('accounts/logout/',signout_view,name='signout'),
    path('task/update/<int:id>/',TaskUpdateView.as_view(),name='todo-update')

]
