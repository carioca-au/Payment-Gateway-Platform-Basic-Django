from django.contrib.auth.forms import UserCreationForm

from payments.models import *


class CreateCompanyForm(UserCreationForm):
    class Meta:
        model = Company

        fields = [
            'name',
            'email',
            'password1',
            'password2'
        ]

        field_order = [
            'name',
            'email',
            'password1',
            'password2'
        ]
