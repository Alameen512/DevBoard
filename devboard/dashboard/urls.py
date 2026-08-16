from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard_view, name='dashboard'),

    # Projects
    path('projects/', views.projects_view, name='projects'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),

    # Tasks
    path('tasks/', views.tasks_view, name='tasks'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:pk>/complete/', views.task_complete, name='task_complete'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),

    # Activity
    path('activity/', views.activity_view, name='activity'),

    # GitHub
    path('github/', views.github_view, name='github'),

    # Analytics
    path('analytics/', views.analytics_view, name='analytics'),

    # Profile
    path('profile/', views.profile_view, name='profile'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
