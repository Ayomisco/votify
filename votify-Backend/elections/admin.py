from django.contrib import admin
from django.utils.html import format_html
from .models import Election, Candidate, Vote


class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 1
    fields = ['full_name', 'department', 'school_level', 'position',
              'about', 'manifesto', 'image']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'election_type', 'department',
                    'start_date', 'end_date', 'created_at', 'updated_at')
    list_filter = ('election_type', 'department', 'start_date', 'end_date')
    search_fields = ('title',)
    ordering = ('-start_date',)
    date_hierarchy = 'start_date'
    readonly_fields = ('created_at', 'updated_at')
    # Ensure CandidateInline is correctly referenced
    inlines = [CandidateInline]


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'department', 'school_level', 'position',
                    'election', 'candidate_image', 'created_at', 'updated_at')
    list_filter = ('department', 'school_level', 'position', 'election')
    search_fields = ('full_name', 'position')
    ordering = ('full_name',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

    def candidate_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    candidate_image.short_description = 'Image'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'candidate', 'election', 'created_at')
    list_filter = ('election', 'created_at')
    search_fields = ('user__username', 'candidate__full_name',
                     'election__title')
    readonly_fields = ('created_at',)
