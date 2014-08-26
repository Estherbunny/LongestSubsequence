from django.db import models
from django import forms
from django.core.validators import RegexValidator

""" The NumberForm is the form on the main page which takes the user """
"""   input, as a comma-separated integer list                       """
class NumberForm(forms.Form):
    number_list = forms.CharField(label='',
        widget=forms.widgets.Textarea(attrs={'rows':6,'cols':70,'placeholder':'4,2,6,3'}),
        validators=[
            RegexValidator(
                regex='^[\d,\-\s]+$',
                message='Only numbers, spaces, and commas are allowed.',
                code='Invalid input'),
            ],)

