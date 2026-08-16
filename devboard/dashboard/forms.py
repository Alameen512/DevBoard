from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from .models import Project, Task, Profile


# ------------------------------------------------------------------
# Small helper: every text-like widget gets Bootstrap's form-control
# class so the whole app stays visually consistent without repeating
# `class="form-control"` on every single field declaration below.
# ------------------------------------------------------------------
BOOTSTRAP_INPUT = 'form-control'
BOOTSTRAP_SELECT = 'form-select'
BOOTSTRAP_CHECK = 'form-check-input'


class RegisterForm(UserCreationForm):
    """Sign-up form: Django's UserCreationForm + an email field."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': BOOTSTRAP_INPUT,
                'placeholder': field.label,
            })


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'progress', 'technologies', 'github_url', 'live_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': BOOTSTRAP_INPUT, 'placeholder': 'e.g. DevBoard'}),
            'description': forms.Textarea(attrs={'class': BOOTSTRAP_INPUT, 'rows': 3, 'placeholder': 'What does this project do?'}),
            'status': forms.Select(attrs={'class': BOOTSTRAP_SELECT}),
            'progress': forms.NumberInput(attrs={'class': BOOTSTRAP_INPUT, 'min': 0, 'max': 100}),
            'technologies': forms.TextInput(attrs={'class': BOOTSTRAP_INPUT, 'placeholder': 'Django, Bootstrap, SQLite'}),
            'github_url': forms.URLInput(attrs={'class': BOOTSTRAP_INPUT, 'placeholder': 'https://github.com/you/project'}),
            'live_url': forms.URLInput(attrs={'class': BOOTSTRAP_INPUT, 'placeholder': 'https://your-demo-link.com'}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'priority', 'status', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': BOOTSTRAP_INPUT, 'placeholder': 'e.g. Fix sidebar collapse bug'}),
            'description': forms.Textarea(attrs={'class': BOOTSTRAP_INPUT, 'rows': 2, 'placeholder': 'Optional details'}),
            'project': forms.Select(attrs={'class': BOOTSTRAP_SELECT}),
            'priority': forms.Select(attrs={'class': BOOTSTRAP_SELECT}),
            'status': forms.Select(attrs={'class': BOOTSTRAP_SELECT}),
            'due_date': forms.DateInput(attrs={'class': BOOTSTRAP_INPUT, 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        # Only show the current user's own projects in the dropdown.
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['project'].queryset = Project.objects.filter(owner=user)
        self.fields['project'].required = False


class ProfileForm(forms.ModelForm):
    """Edits the Profile model (avatar, bio, skills, GitHub handle)."""
    first_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': BOOTSTRAP_INPUT}))
    last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': BOOTSTRAP_INPUT}))

    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'skills', 'github_username']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': BOOTSTRAP_INPUT, 'rows': 3, 'placeholder': 'A short bio about you'}),
            'skills': forms.TextInput(attrs={'class': BOOTSTRAP_INPUT, 'placeholder': 'Python, Django, JavaScript'}),
            'github_username': forms.TextInput(attrs={'class': BOOTSTRAP_INPUT, 'placeholder': 'octocat'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            profile.user.first_name = self.cleaned_data.get('first_name', '')
            profile.user.last_name = self.cleaned_data.get('last_name', '')
            profile.user.save()
        return profile


class AccountForm(forms.ModelForm):
    """Settings > Account: change username / email."""
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': BOOTSTRAP_INPUT}),
            'email': forms.EmailInput(attrs={'class': BOOTSTRAP_INPUT}),
        }


class NotificationSettingsForm(forms.ModelForm):
    """Settings > Notifications."""
    class Meta:
        model = Profile
        fields = ['email_notifications', 'task_reminders', 'project_update_notifications']
        widgets = {
            'email_notifications': forms.CheckboxInput(attrs={'class': BOOTSTRAP_CHECK}),
            'task_reminders': forms.CheckboxInput(attrs={'class': BOOTSTRAP_CHECK}),
            'project_update_notifications': forms.CheckboxInput(attrs={'class': BOOTSTRAP_CHECK}),
        }


class AppearanceSettingsForm(forms.ModelForm):
    """Settings > Appearance (dark / light mode)."""
    class Meta:
        model = Profile
        fields = ['dark_mode']
        widgets = {
            'dark_mode': forms.CheckboxInput(attrs={'class': BOOTSTRAP_CHECK, 'role': 'switch'}),
        }


class DevBoardPasswordChangeForm(PasswordChangeForm):
    """PasswordChangeForm with Bootstrap-styled widgets."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': BOOTSTRAP_INPUT})
