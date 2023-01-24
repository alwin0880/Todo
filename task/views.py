from django.shortcuts import render,redirect
from django.views.generic import View,ListView,DetailView,UpdateView

from task.models import Task

from task.forms import RegistrationForm,LoginForm,TaskUpdateForm

from django.urls import reverse_lazy

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from django.utils.decorators import method_decorator

# Create your views here.


def signin_reqired(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


class IndexView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"index.html")


class LoginView1(View):
     def get(self,request,*args,**kwargs):
        return render(request,"task-log.html")

@method_decorator(signin_reqired,name='dispatch')
class AddTaskView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"todo.html")
    
    def post(self,request,*args,**kwargs):
        user=request.user  
        task=request.POST.get("task")                           #same name as given in html page
        Task.objects.create(user=user,task_name=task)
        messages.success(request,'task has been created')
        return redirect("todo-all")

@method_decorator(signin_reqired,name='dispatch')
class TaskListView(ListView):
    model=Task
    template_name='task-list.html'
    context_object_name='todos'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    # def get(self,request,*args,**kwargs):
    #     if request.user.is_authenticated:
    #         qs=Task.objects.filter(user=request.user)
    #                  # or
    #         # qs=request.user.task_all()
    #         return render(request,"task-list.html",{"todos":qs})
    #     else:
    #         return redirect("signin")


@method_decorator(signin_reqired,name='dispatch')
class TaskDetailView(DetailView):
    model=Task
    template_name='task-detail.html'
    context_object_name='todo'
    pk_url_kwarg='id'


    # def get(self,request,*args,**kwargs):                     #View use cheyth 
    #     id=kwargs.get("id")
    #     task=Task.objects.get(id=id)
    #     return render(request,"task-detail.html",{"todo":task})
    

@method_decorator(signin_reqired,name='dispatch')
class TaskDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Task.objects.filter(id=id).delete()
        messages.success(request,'task deleted')
        return redirect("todo-all")


class RegistrationView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,'register.html',{'form':form})


    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,'account created')
            return redirect('signin')
        else:
            messages.success(request,'registration failed')
            return render(request,'register.html',{'form':form})


class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{'form':form})


    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,'login successfully')
                return redirect('todo-all')
            else:
                messages.success(request,'invalid username or password')
                return render(request,'login.html',{'form':form})

@signin_reqired          #fn aya karanam
def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")



class TaskUpdateView(UpdateView):
    model=Task
    template_name="task-update.html"
    form_class=TaskUpdateForm
    pk_url_kwarg="id"
    success_url=reverse_lazy('todo-all')
    