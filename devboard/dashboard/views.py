import calendar
import json
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import (
    RegisterForm, ProjectForm, TaskForm, ProfileForm,
    AccountForm, NotificationSettingsForm, AppearanceSettingsForm,
)
from .models import Project, Task, Activity, Profile


# ------------------------------------------------------------------
# Small helpers shared by several views
# ------------------------------------------------------------------
def log_activity(user, activity_type, description):
    """Create an Activity record — called after key user actions."""
    Activity.objects.create(user=user, activity_type=activity_type, description=description)


def update_streak(profile):
    """
    Recalculates the user's productivity streak. Called whenever a
    task is marked completed. If the user's last completion was
    yesterday, the streak grows; if it was earlier than that, the
    streak resets to 1; if it was already today, nothing changes.
    """
    today = timezone.localdate()
    if profile.last_activity_date == today:
        return
    elif profile.last_activity_date == today - timedelta(days=1):
        profile.current_streak += 1
    else:
        profile.current_streak = 1
    profile.last_activity_date = today
    profile.longest_streak = max(profile.longest_streak, profile.current_streak)
    profile.save()


def weekly_productivity(user):
    """
    Returns a list of {day, count} for the current week (Mon-Sun),
    counting tasks the user completed on each day. Powers the
    dashboard + analytics charts.
    """
    today = timezone.localdate()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    data = []
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        count = Task.objects.filter(
            owner=user, status=Task.STATUS_COMPLETED,
            completed_at__date=day
        ).count()
        data.append({'day': calendar.day_name[day.weekday()][:3], 'count': count})
    return data


# ------------------------------------------------------------------
# Authentication
# ------------------------------------------------------------------
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            log_activity(user, Activity.TYPE_PROFILE_UPDATED, 'Welcome to DevBoard! Account created.')
            messages.success(request, f'Welcome to DevBoard, {user.username}!')
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Good to see you again, {user.username}.')
            next_url = request.GET.get('next') or 'dashboard'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out. See you soon!')
    return redirect('login')


# ------------------------------------------------------------------
# Dashboard
# ------------------------------------------------------------------
@login_required
def dashboard_view(request):
    user = request.user
    profile = user.profile

    projects = Project.objects.filter(owner=user)
    tasks = Task.objects.filter(owner=user)

    context = {
        'total_projects': projects.count(),
        'completed_tasks': tasks.filter(status=Task.STATUS_COMPLETED).count(),
        'total_tasks': tasks.count(),
        'current_streak': profile.current_streak,
        'github_contributions': 128,  # mock value — swap for a real GitHub API call later
        'weekly_data_json': json.dumps(weekly_productivity(user)),
        'recent_activity': Activity.objects.filter(user=user)[:6],
        'recent_projects': projects[:3],
        'today': timezone.localdate(),
    }
    return render(request, 'dashboard.html', context)


# ------------------------------------------------------------------
# Projects
# ------------------------------------------------------------------
@login_required
def projects_view(request):
    projects = Project.objects.filter(owner=request.user)
    context = {
        'projects': projects,
        'form': ProjectForm(),
    }
    return render(request, 'projects.html', context)


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            log_activity(request.user, Activity.TYPE_PROJECT_CREATED, f'Created project "{project.name}"')
            messages.success(request, f'Project "{project.name}" created.')
        else:
            messages.error(request, 'Please fix the errors in the project form.')
    return redirect('projects')


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            log_activity(request.user, Activity.TYPE_PROJECT_UPDATED, f'Updated project "{project.name}"')
            messages.success(request, f'Project "{project.name}" updated.')
        else:
            messages.error(request, 'Please fix the errors in the project form.')
    return redirect('projects')


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == 'POST':
        name = project.name
        project.delete()
        log_activity(request.user, Activity.TYPE_PROJECT_DELETED, f'Deleted project "{name}"')
        messages.info(request, f'Project "{name}" deleted.')
    return redirect('projects')


# ------------------------------------------------------------------
# Tasks
# ------------------------------------------------------------------
@login_required
def tasks_view(request):
    tasks = Task.objects.filter(owner=request.user)
    context = {
        'tasks': tasks,
        'form': TaskForm(user=request.user),
        'user_projects': Project.objects.filter(owner=request.user),
        'todo_count': tasks.filter(status=Task.STATUS_TODO).count(),
        'in_progress_count': tasks.filter(status=Task.STATUS_IN_PROGRESS).count(),
        'completed_count': tasks.filter(status=Task.STATUS_COMPLETED).count(),
    }
    return render(request, 'tasks.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            log_activity(request.user, Activity.TYPE_TASK_CREATED, f'Added task "{task.title}"')
            messages.success(request, f'Task "{task.title}" added.')
        else:
            messages.error(request, 'Please fix the errors in the task form.')
    return redirect('tasks')


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" updated.')
        else:
            messages.error(request, 'Please fix the errors in the task form.')
    return redirect('tasks')


@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        task.mark_completed()
        update_streak(request.user.profile)
        log_activity(request.user, Activity.TYPE_TASK_COMPLETED, f'Completed task "{task.title}"')
        messages.success(request, f'Nice work — "{task.title}" marked complete!')
    return redirect('tasks')


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        title = task.title
        task.delete()
        log_activity(request.user, Activity.TYPE_TASK_DELETED, f'Deleted task "{title}"')
        messages.info(request, f'Task "{title}" deleted.')
    return redirect('tasks')


# ------------------------------------------------------------------
# Activity feed
# ------------------------------------------------------------------
@login_required
def activity_view(request):
    activities = Activity.objects.filter(user=request.user)
    return render(request, 'activity.html', {'activities': activities})


# ------------------------------------------------------------------
# GitHub (mock data — structured so it's a one-function swap later)
# ------------------------------------------------------------------
def get_github_data(username):
    """
    Returns mock GitHub profile data shaped exactly like what
    api.github.com/users/<username> and .../repos would return.
    To go live: swap this function's body for `requests.get(...)`
    calls to the real GitHub REST API and map the JSON the same way.
    """
    return {
        'username': username or 'devboard-user',
        'repos': 24,
        'followers': 312,
        'following': 87,
        'primary_language': 'Python',
        'recent_repos': [
            {'name': 'devboard', 'description': 'Developer productivity dashboard', 'stars': 42, 'language': 'Python'},
            {'name': 'student-management-system', 'description': 'Django app for schools', 'stars': 18, 'language': 'Python'},
            {'name': 'portfolio-website', 'description': 'Personal portfolio site', 'stars': 9, 'language': 'HTML'},
            {'name': 'weather-app', 'description': 'Weather forecast web app', 'stars': 15, 'language': 'JavaScript'},
            {'name': 'expense-tracker', 'description': 'Track daily expenses', 'stars': 11, 'language': 'JavaScript'},
        ],
    }


@login_required
def github_view(request):
    profile = request.user.profile
    context = {'github': get_github_data(profile.github_username)}
    return render(request, 'github.html', context)


# ------------------------------------------------------------------
# Analytics
# ------------------------------------------------------------------
@login_required
def analytics_view(request):
    user = request.user
    tasks = Task.objects.filter(owner=user)
    projects = Project.objects.filter(owner=user)
    profile = user.profile

    status_breakdown = {
        'todo': tasks.filter(status=Task.STATUS_TODO).count(),
        'in_progress': tasks.filter(status=Task.STATUS_IN_PROGRESS).count(),
        'completed': tasks.filter(status=Task.STATUS_COMPLETED).count(),
    }

    project_progress = [{'name': p.name, 'progress': p.progress} for p in projects]

    context = {
        'weekly_data_json': json.dumps(weekly_productivity(user)),
        'status_breakdown': status_breakdown,
        'status_breakdown_json': json.dumps(status_breakdown),
        'project_progress': project_progress,
        'project_progress_json': json.dumps(project_progress),
        'current_streak': profile.current_streak,
        'longest_streak': profile.longest_streak,
        'total_tasks': tasks.count(),
        'completed_tasks': status_breakdown['completed'],
    }
    return render(request, 'analytics.html', context)


# ------------------------------------------------------------------
# Profile
# ------------------------------------------------------------------
@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            log_activity(request.user, Activity.TYPE_PROFILE_UPDATED, 'Updated profile information')
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile})


# ------------------------------------------------------------------
# Settings
# ------------------------------------------------------------------
@login_required
def settings_view(request):
    profile = request.user.profile
    account_form = AccountForm(instance=request.user)
    notif_form = NotificationSettingsForm(instance=profile)
    appearance_form = AppearanceSettingsForm(instance=profile)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        section = request.POST.get('form_section')

        if section == 'account':
            account_form = AccountForm(request.POST, instance=request.user)
            if account_form.is_valid():
                account_form.save()
                messages.success(request, 'Account details updated.')
                return redirect('settings')

        elif section == 'notifications':
            notif_form = NotificationSettingsForm(request.POST, instance=profile)
            if notif_form.is_valid():
                notif_form.save()
                messages.success(request, 'Notification preferences saved.')
                return redirect('settings')

        elif section == 'appearance':
            appearance_form = AppearanceSettingsForm(request.POST, instance=profile)
            if appearance_form.is_valid():
                appearance_form.save()
                messages.success(request, 'Appearance updated.')
                return redirect('settings')

        elif section == 'password':
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # keep the user logged in
                messages.success(request, 'Password changed successfully.')
                return redirect('settings')

        messages.error(request, 'Please fix the errors below.')

    context = {
        'account_form': account_form,
        'notif_form': notif_form,
        'appearance_form': appearance_form,
        'password_form': password_form,
        'profile': profile,
    }
    return render(request, 'settings.html', context)
