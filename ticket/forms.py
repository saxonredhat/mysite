from django.forms import ModelForm
from django import forms
from ticket.models import *
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = _('清除')
    initial_text = _('当前')
    input_text = _('改变')
    template_name = 'ticket/clearable_file_input.html'


class MySelect(forms.Select):
    def render_option(self, selected_choices, option_value, option_label):
        return u'<option whatever>...</option>'


class TicketForm(ModelForm):
    vcs_tag = forms.CharField(widget=forms.Select(choices=[]), label="分支或标签", required=False)

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
        self.fields['service'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['vcs_tag'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['test_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['audit_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['execute_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['service_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 5
        }
        self.fields['db_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 8
        }
        self.fields['db_file'].widget.attrs = {
            'class': 'form-control',
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
            'db_file': CustomClearableFileInput
        }
        help_texts = {
        }
        error_messages = {
            'title': {
                'max_length': _("This writer's name is too long."),
            },
        }


class TicketFromTicketForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TicketFromTicketForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['title'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['space'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['service'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['vcs_tag'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['test_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['audit_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['execute_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['service_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 5,
            'disabled': True
        }
        self.fields['db_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 8,
            'disabled': True
        }
        self.fields['db_file'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['other_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 2,
            'disabled': True
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
            'db_file': CustomClearableFileInput
        }
        help_texts = {
        }
        error_messages = {
            'title': {
                'max_length': _("This writer's name is too long."),
            },
        }


class TicketUpdateForm(ModelForm):
    #vcs_tag = forms.CharField(widget=forms.Select(choices=[]), label="标签版本",required=False)
    def __init__(self, *args, **kwargs):
        super(TicketUpdateForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['title'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['space'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['service'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['vcs_tag'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['test_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['audit_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['execute_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['service_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 5
        }
        self.fields['db_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 8
        }
        self.fields['db_file'].widget.attrs = {
            'class': 'form-control',
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
            'db_file': CustomClearableFileInput,
        }
        help_texts = {
        }
        error_messages = {
            'title': {
                'max_length': _("This writer's name is too long."),
            },
        }



class TicketAuditForm(ModelForm):
    status = forms.ChoiceField(choices=[(11,'审核通过'),(12,'审核不通过')])

    def __init__(self, *args, **kwargs):
        super(TicketAuditForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['title'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['space'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['service'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['vcs_tag'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['test_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['audit_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['execute_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['service_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 5,
            'disabled': True
        }
        self.fields['db_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 8,
            'disabled': True
        }
        self.fields['other_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 2,
            'disabled': True
        }
        self.fields['audit_description'].widget.attrs = {
            'class': 'form-control',
            'rows': 8
        }
        self.fields['status'].widget.attrs = {
            'class': 'form-control'
        }

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


class TicketCancelForm(ModelForm):
    status = forms.ChoiceField(choices=[(-1, '作废')])

    def __init__(self, *args, **kwargs):
        super(TicketCancelForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['title'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['space'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['service'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['vcs_tag'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['test_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['audit_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['execute_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['service_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 5,
            'disabled': True
        }
        self.fields['db_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 8,
            'disabled': True
        }
        self.fields['other_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 2,
            'disabled': True
        }
        self.fields['cancel_description'].widget.attrs = {
            'class': 'form-control',
            'rows': 8
        }
        self.fields['status'].widget.attrs = {
            'class': 'form-control'
        }

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



class TicketExecuteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TicketExecuteForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['title'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['space'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['service'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['vcs_tag'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['test_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['audit_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['execute_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['service_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 5,
            'disabled': True
        }
        self.fields['db_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 8,
            'disabled': True
        }
        self.fields['other_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 2,
            'disabled': True
        }
        self.fields['execute_description'].widget.attrs = {
            'class': 'form-control',
            'rows': 8
        }

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


class TicketTestForm(ModelForm):
    status = forms.ChoiceField(choices=[(31,'测试通过'),(32,'测试不通过')])

    def __init__(self, *args, **kwargs):
        super(TicketTestForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['title'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['space'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['service'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['vcs_tag'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['test_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['audit_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['execute_user'].widget.attrs = {
            'class': 'form-control',
            'disabled': True
        }
        self.fields['service_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 5,
            'disabled': True
        }
        self.fields['db_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 8,
            'disabled': True
        }
        self.fields['other_conf'].widget.attrs = {
            'class': 'form-control',
            'rows': 2,
            'disabled': True
        }
        self.fields['test_description'].widget.attrs = {
            'class': 'form-control',
            'rows': 8
        }
        self.fields['status'].widget.attrs = {
            'class': 'form-control'
        }

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