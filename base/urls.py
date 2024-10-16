from django.urls import path, include
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, UserLogin, custom_logout_view, TaskListCreate, TaskRetrieveUpdateDestroy, TaskViewSet
from django.contrib.auth.views import LogoutView
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Tasks', TaskViewSet)



urlpatterns = [
    # path('', include(router.urls)),
    path('api/tasks/', TaskListCreate.as_view(), name = 'task-list-create'),
    path('api/tasks/<int:pk>/', TaskRetrieveUpdateDestroy.as_view(), name = 'task-detail'),
    path('register/', views.register, name = 'register'),
    path('login/', UserLogin.as_view(), name = 'login'),
    path('logout/', custom_logout_view, name = 'logout'),
    path('', TaskList.as_view(), name = 'tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name = 'details' ),
    path('task-create/', TaskCreate.as_view(), name = 'task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name = 'task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name = 'task-delete'),
]
