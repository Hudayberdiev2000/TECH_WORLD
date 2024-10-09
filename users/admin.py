from django.contrib import admin
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken


class CustomOutstandingTokenAdmin(OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, CustomOutstandingTokenAdmin)

from .models import User, Adddress

class AddressInline(admin.StackedInline):
    model = Adddress
    extra = 1

class PasswordUserAdmin(admin.ModelAdmin):
    inlines = [AddressInline]
    list_display = ('id', 'full_name', 'phone_number', 'is_staff', 'is_active')

    def save_model(self, request, obj, form, change):
        # Only set the password if it's a new user
        if not change:
            obj.password = make_password(obj.password)

        obj.user = request.user
        obj.save()

admin.site.register(User, PasswordUserAdmin)