from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Department
from .forms import CustomUserCreationForm, CustomUserChangeForm


    


class UserAdmin(BaseUserAdmin):

    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    # Define which fields to display on the admin interface
    list_display = ('email', 'full_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'user_type')
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    actions = ['mark_active']  # Custom actions

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_active.short_description = "Mark selected users as active"

    # Define fields for creating and editing users
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': ('full_name', 'school_level', 'department', 'profile_pic', 'matriculation_number', 'user_type')
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('matriculation_number', 'full_name', 'department', 'school_level', 'email', 'password', 'confirm_password', 'is_staff', 'user_type')
        }),
    )


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields.pop('is_superuser', None)
        return form

    def has_add_permission(self, request):
        # Restrict user creation to superusers only
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        # Allow admins to change users, but not superusers
        if request.user.is_superuser:
            return True
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        # Allow admins to delete users, but not superusers
        if request.user.is_superuser:
            return True
        return super().has_delete_permission(request, obj)

    search_fields = ('email', 'full_name')
    ordering = ('email',)
    filter_horizontal = ()


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)


admin.site.site_header = "Votify Admin Portal"
admin.site.site_title = "Votify Admin Portal"
admin.site.index_title = "Welcome to Votify Admin Portal"

admin.site.register(User, UserAdmin)
admin.site.register(Department, DepartmentAdmin)
