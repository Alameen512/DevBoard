from django.contrib import admin
from .models import Profile, Project, Task, Activity


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'github_username', 'current_streak', 'longest_streak', 'dark_mode', 'created_at')
    search_fields = ('user__username', 'user__email', 'github_username')
    list_filter = ('dark_mode', 'email_notifications')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'progress', 'task_count', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'description', 'technologies', 'owner__username')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    @admin.display(description='Tasks')
    def task_count(self, obj):
        return obj.task_count


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'project', 'priority', 'status', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'due_date')
    search_fields = ('title', 'description', 'owner__username')
    ordering = ('-created_at',)
    list_editable = ('status', 'priority')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'description', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('description', 'user__username')
    ordering = ('-created_at',)


# Custom admin site branding
admin.site.site_header = 'DevBoard Administration'
admin.site.site_title = 'DevBoard Admin'
admin.site.index_title = 'Manage Users, Projects, Tasks & Activity'
