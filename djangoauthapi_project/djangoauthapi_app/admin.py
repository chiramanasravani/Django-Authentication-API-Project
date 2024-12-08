from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserModelAdmin
from djangoauthapi_app.models import User

class UserModelAdmin(BaseUserModelAdmin):
    # The fields to be used in displaying the User model.
    list_display = ["id", "email", "name", "tc", "is_admin"]
    list_filter = ["is_admin"]
    
    fieldsets = [
        (None, {"fields": ["email", "password"]}),  # Corrected this line
        ("Personal info", {"fields": ["name", "tc"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "tc", "password1", "password2"],
            },
        ),
    ]
    
    search_fields = ["email"]
    ordering = ["email", "id"]
    filter_horizontal = ()

# Register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)














