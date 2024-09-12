from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone  # Add this import
from .models import Election, Candidate, Vote
from .forms import CandidateForm
from django import forms


class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError(
                    "End date must be after the start date.")

        return cleaned_data


class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 1
    fields = ['full_name', 'department',
              'school_level', 'about', 'manifesto', 'image']
    readonly_fields = ['created_at', 'updated_at']


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
            # Logic for new elections
            obj.created_at = timezone.now()  # Use timezone now
        obj.updated_at = timezone.now()  # Use timezone now
        super().save_model(request, obj, form, change)

    def election_type(self, obj):
        return obj.get_election_type_display()
    election_type.short_description = 'Election Type'

    # Custom actions
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
    form = CandidateForm  # Use the custom form
    list_display = ('full_name', 'department', 'school_level',
                    'election', 'candidate_image', 'created_at', 'updated_at')
    list_filter = ('department', 'school_level', 'election')
    search_fields = ('full_name', 'department')
    ordering = ('full_name',)
    date_hierarchy = 'created_at'
    # Make votes_count readonly
    readonly_fields = ('created_at', 'updated_at', 'votes_count')

    def candidate_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    candidate_image.short_description = 'Image'


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['candidate', 'election']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        candidate = cleaned_data.get("candidate")
        election = cleaned_data.get("election")

        if self.user and candidate and election:
            if candidate.user != self.user:
                raise forms.ValidationError("You can only vote for yourself.")
            if Vote.objects.filter(user=self.user, election=election).exists():
                raise forms.ValidationError(
                    "You have already voted in this election.")

        return cleaned_data


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    form = VoteForm
    list_display = ('user', 'candidate', 'election', 'created_at')
    list_filter = ('election', 'created_at')
    search_fields = ('user__username', 'candidate__full_name',
                     'election__election_type')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:  # Admin can only vote for themselves
            obj.user = request.user
        super().save_model(request, obj, form, change)
