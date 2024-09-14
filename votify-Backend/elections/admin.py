# admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Election, Candidate, Vote
from .forms import CandidateForm, ElectionForm, VoteForm


class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 0  # Don't add extra blank candidates
    fields = ('full_name', 'matriculation_number', 'votes_count')
    readonly_fields = ('full_name', 'matriculation_number', 'votes_count')
    can_delete = False
    min_num = 0
    max_num = None

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    form = ElectionForm
    list_display = ('election_type', 'start_date', 'end_date',
                    'status', 'created_at', 'updated_at')
    list_filter = ('election_type', 'status', 'start_date', 'end_date')
    search_fields = ('election_type',)
    ordering = ('-start_date',)
    date_hierarchy = 'start_date'
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CandidateInline]

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == 'Finished':
            return self.readonly_fields + ('election_type', 'start_date', 'end_date', 'status')
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_at = timezone.now()
        obj.updated_at = timezone.now()
        super().save_model(request, obj, form, change)

    actions = ['mark_as_active', 'mark_as_upcoming', 'mark_as_finished']

    def mark_as_active(self, request, queryset):
        updated_count = queryset.update(status='Active')
        self.message_user(
            request, f"{updated_count} elections marked as active.")
    mark_as_active.short_description = 'Mark selected elections as Active'

    def mark_as_upcoming(self, request, queryset):
        updated_count = queryset.update(status='Upcoming')
        self.message_user(
            request, f"{updated_count} elections marked as upcoming.")
    mark_as_upcoming.short_description = 'Mark selected elections as Upcoming'

    def mark_as_finished(self, request, queryset):
        updated_count = queryset.update(status='Finished')
        self.message_user(
            request, f"{updated_count} elections marked as finished.")
    mark_as_finished.short_description = 'Mark selected elections as Finished'


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    form = CandidateForm
    list_display = ('election', 'full_name', 'department', 'school_level',
                    'matriculation_number', 'candidate_image', 'created_at', 'updated_at')
    list_filter = ('election', 'department', 'school_level')
    search_fields = ('full_name', 'department', 'matriculation_number')
    ordering = ('election', 'full_name')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    exclude = ('votes_count',)

    def candidate_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    candidate_image.short_description = 'Image'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    form = VoteForm
    list_display = ('user', 'candidate', 'election', 'voted_at')
    list_filter = ('election', 'voted_at')
    search_fields = ('user__username', 'candidate__full_name',
                     'election__election_type')
    readonly_fields = ('user', 'candidate', 'election', 'voted_at')
    ordering = ('-voted_at',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass  # No saving allowed
