from django.core.exceptions import ValidationError
from django.contrib import admin
from django.utils.html import format_html
from .models import Election, Candidate, Vote
from django.core.files.images import get_image_dimensions


class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 1
    fields = ['full_name', 'department',
              'school_level', 'about', 'manifesto', 'image']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('election_type', 'department', 'start_date',
                    'end_date', 'status', 'created_at', 'updated_at')
    list_filter = ('election_type', 'department',
                   'status', 'start_date', 'end_date')
    search_fields = ('election_type',)
    ordering = ('-start_date',)
    date_hierarchy = 'start_date'
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CandidateInline]


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'department', 'school_level',
                    'election', 'candidate_image', 'created_at', 'updated_at')
    list_filter = ('department', 'school_level', 'election')
    search_fields = ('full_name', 'election__election_type')
    ordering = ('full_name',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

    def candidate_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    candidate_image.short_description = 'Image'

    def save_model(self, request, obj, form, change):
        # Validate the image file if it's provided
        if obj.image:
            try:
                width, height = get_image_dimensions(obj.image)
            except Exception:
                raise ValidationError(
                    "Uploaded file is not a valid image. Please upload a valid image (JPEG, PNG, etc.).")
        super().save_model(request, obj, form, change)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'candidate', 'election', 'created_at')
    list_filter = ('election', 'created_at')
    search_fields = ('user__username', 'candidate__full_name',
                     'election__election_type')
    readonly_fields = ('created_at',)
