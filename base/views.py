from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy


from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.contrib import messages

from .models import Task
from .forms import RegisterForm


from rest_framework import generics, viewsets
from .serializers import TaskSerializer


# Create your views here.

class UserLogin(LoginView):
    model = Task
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')




class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'   # to change the object name to be used in templates

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user = self.request.user)
        context["count"] = context["tasks"].filter(complete  = False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context["tasks"] = context["tasks"].filter(title__icontains=search_input)

        context["search_input"] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html' # to change the file name in templates

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description", "complete"] # instead of fields, we also can use form_class = TaskForm
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):                  # to make only registered user can create their own post
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title", "description", "complete"]
    success_url = reverse_lazy("tasks")

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy("tasks")


def custom_logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid:
            user = form.save()
            login(request, user)
            return redirect('tasks') # Redirect to a home page or dashboard
    else:
        form = RegisterForm()
    return render(request, 'base/register.html', {'form': form})



# Create API views
class TaskListCreate(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
