from django.forms import ModelForm
from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import ClearableFileInput


class JobForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['description'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['space'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['service'].widget.attrs = {
            'class': 'form-control'
        }

    class Meta:
        model = Job
        fields = '__all__'
        labels = {
        }
        widgets = {
        }
        help_texts = {
        }
        error_messages = {
            'title': {
                'max_length': _("This writer's name is too long."),
            },
        }


class JobUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(JobUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['description'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['space'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['service'].widget.attrs = {
            'class': 'form-control'
        }

    class Meta:
        model = Job
        fields = '__all__'


class JobPlanForm(ModelForm):
    project = forms.CharField(label="项目", required=False)
    service = forms.CharField(label="服务", required=False)
    vcs_tag = forms.CharField(widget=forms.Select(choices=[]), label="分支或标签版本", required=False)

    def __init__(self, *args, **kwargs):
        super(JobPlanForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['job'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['vcs_tag'].widget.attrs = {
            'class': 'form-control'
        }

        self.fields['job_type'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }

        self.fields['project'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }

        self.fields['service'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }

        self.fields['created_type'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }

    class Meta:
        model = JobPlan
        fields = '__all__'
        labels = {
        }
        widgets = {
        }
        help_texts = {
        }
        error_messages = {
            'title': {
                'max_length': _("This writer's name is too long."),
            },
        }




class JobPlanUpdateForm(ModelForm):
    class Meta:
        model = JobPlan
        fields = '__all__'