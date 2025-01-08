from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import UserModel

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified', 'groups')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'pfp')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'created', 'modified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'groups',
                       'is_active', 'is_staff'),
        }),
    )
    search_fields = ('id', 'email', 'first_name', 'last_name', 'phone_number')
    readonly_fields = ('last_login', 'created', 'modified')
    ordering = ()
    date_hierarchy = 'created'
    actions = ['activate_users', ]
    save_on_top = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('auth.change_user'):
            del actions['activate_users']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        if not is_superuser:
            disabled_fields |= {
                'is_superuser',
                'user_permissions',
            }

        if (not is_superuser and obj is not None and obj == request.user):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form

    def save_model(self, request, obj, form, change):
        obj.email = obj.email.lower()
        return super(UserAdmin, self).save_model(request, obj, form, change)


admin.site.register(UserModel, CustomUserAdmin)