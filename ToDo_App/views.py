from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import*

# Create your views here.
class LogIn(LoginView):
    template_name='login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    
    
class RegisterPage(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url=reverse_lazy('tasks')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)
    

class TaskView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name= 'tasks'
    template_name= 'task_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(status = False).count()
        
        search_input = self.request.GET.get('search') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__startswith = search_input)
        context['search_input']=search_input
        return context
    
    
    
class taskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name ='task.html'
    
class createTask(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'status']
    success_url=reverse_lazy('tasks') 
    template_name = 'create.html'
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(createTask, self).form_valid(form)
    
    
class UpdateTask(LoginRequiredMixin, UpdateView):
    model = Task
    fields =     fields = ['title', 'description', 'status']
    template_name='create.html'
    success_url = reverse_lazy('tasks')
    
    
class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name='task'
    template_name='delete.html'
    success_url=reverse_lazy('tasks')
