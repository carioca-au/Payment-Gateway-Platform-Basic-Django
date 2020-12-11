from django.contrib import admin
from abc import ABC

from django.contrib.auth.admin import UserAdmin

from payments.models import *


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter, ABC):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


admin.site.register(Company, UserAdmin)
admin.site.register(Bank)
admin.site.register(Account)
admin.site.register(Payment)
