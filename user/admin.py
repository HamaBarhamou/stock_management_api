# Register your models here.
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class CustumerUser(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['pk',
                    'email',
                    'username',
                    'first_name',
                    'last_name',
                    'fonction'
                    ]
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None,
            {'fields': (
                        'email',
                        'first_name',
                        'last_name',
                        'fonction',
                        'avatar'
                        )
             }
         ),
    )
    fieldsets = UserAdmin.fieldsets


admin.site.register(User, CustumerUser)