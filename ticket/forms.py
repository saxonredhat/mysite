from django.forms import ModelForm
from django import forms
from ticket.models import *
from django.utils.translation import gettext_lazy as _



class TicketForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['title'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['space'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['project'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['vcs_tag'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['test_user'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['audit_user'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['execute_user'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['service_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 5
        }
        self.fields['db_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 8
        }
        self.fields['other_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 2
        }
        self.fields['test_user'].queryset = self.fields['test_user'].queryset.filter(position__name='测试人员')
        self.fields['audit_user'].queryset = self.fields['audit_user'].queryset.filter(position__name='审核人员')
        self.fields['execute_user'].queryset = self.fields['execute_user'].queryset.filter(position__name='运维人员')
    class Meta:
        model = Ticket
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