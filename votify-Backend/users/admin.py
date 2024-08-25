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
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('email', 'full_name')
    ordering = ('email',)

    # Define fields for creating and editing users
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
         'fields': ('full_name', 'department', 'profile_pic', 'matriculation_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {
         'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('matriculation_number', 'full_name', 'department', 'email', 'password', 'confirm_password', 'is_staff')}
        ),
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


admin.site.register(User, UserAdmin)
admin.site.register(Department, DepartmentAdmin)
