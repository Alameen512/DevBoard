from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    """
    Extends Django's built-in User model (which already provides
    username, email and a hashed password) with the extra fields
    DevBoard needs: avatar, bio, GitHub handle and streak tracking.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, default='')
    skills = models.CharField(
        max_length=255, blank=True, default='',
        help_text='Comma-separated list, e.g. "Python, Django, JavaScript"'
    )
    github_username = models.CharField(max_length=100, blank=True, default='')

    # Productivity streak tracking (updated whenever a task is completed)
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(blank=True, null=True)

    # Settings (appearance + notifications)
    dark_mode = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    task_reminders = models.BooleanField(default=True)
    project_update_notifications = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def skills_list(self):
        """Return the comma-separated skills field as a clean list."""
        return [s.strip() for s in self.skills.split(',') if s.strip()]


class Project(models.Model):
    STATUS_PLANNED = 'planned'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [
        (STATUS_PLANNED, 'Planned'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PLANNED)
    progress = models.PositiveIntegerField(default=0, help_text='Completion percentage, 0-100')
    technologies = models.CharField(
        max_length=255, blank=True, default='',
        help_text='Comma-separated list, e.g. "Django, Bootstrap, SQLite"'
    )
    github_url = models.URLField(blank=True, default='')
    live_url = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def technologies_list(self):
        return [t.strip() for t in self.technologies.split(',') if t.strip()]

    @property
    def task_count(self):
        return self.tasks.count()

    @property
    def completed_task_count(self):
        return self.tasks.filter(status=Task.STATUS_COMPLETED).count()


class Task(models.Model):
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
    ]

    STATUS_TODO = 'todo'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [
        (STATUS_TODO, 'Todo'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, related_name='tasks', blank=True, null=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_TODO)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def mark_completed(self):
        self.status = self.STATUS_COMPLETED
        self.completed_at = timezone.now()
        self.save()


class Activity(models.Model):
    TYPE_PROJECT_CREATED = 'project_created'
    TYPE_PROJECT_UPDATED = 'project_updated'
    TYPE_PROJECT_DELETED = 'project_deleted'
    TYPE_TASK_CREATED = 'task_created'
    TYPE_TASK_COMPLETED = 'task_completed'
    TYPE_TASK_DELETED = 'task_deleted'
    TYPE_PROFILE_UPDATED = 'profile_updated'
    TYPE_CHOICES = [
        (TYPE_PROJECT_CREATED, 'Project created'),
        (TYPE_PROJECT_UPDATED, 'Project updated'),
        (TYPE_PROJECT_DELETED, 'Project deleted'),
        (TYPE_TASK_CREATED, 'Task created'),
        (TYPE_TASK_COMPLETED, 'Task completed'),
        (TYPE_TASK_DELETED, 'Task deleted'),
        (TYPE_PROFILE_UPDATED, 'Profile updated'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f"{self.get_activity_type_display()}: {self.description}"
