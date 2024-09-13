from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Election, Candidate, Vote
from .forms import CandidateForm
from django import forms


# Election Form (Ensuring Valid Start and End Dates)
class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError(
                "End date must be after the start date.")
        return cleaned_data




class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 0  # Don't add extra blank candidates
    fields = ('full_name', 'matriculation_number', 'votes_count')
    readonly_fields = ('full_name', 'matriculation_number',
                       'votes_count')  # Make fields read-only
    can_delete = False  # Disable deletion via inline
    min_num = 0  # Do not require any candidates to be present
    max_num = None  # No limit to the number of candidates


    def has_add_permission(self, request, obj):
        return False  # Disable adding new candidates

    def has_change_permission(self, request, obj=None):
        return False  # Disable editing existing candidates

    def has_delete_permission(self, request, obj=None):
        return False  # Disable deleting candidates

# Election Admin (Customized List and Candidate Inline)
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

    # Inline Candidates within Election
    inlines = [CandidateInline]

    # Restrict editing based on status (e.g., Finished elections)
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == 'Finished':
            return self.readonly_fields + ('election_type', 'start_date', 'end_date', 'status')
        return self.readonly_fields

    # Save timestamps for elections
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_at = timezone.now()
        obj.updated_at = timezone.now()
        super().save_model(request, obj, form, change)

    # Custom actions for marking election status
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


# Candidate Admin (Customized List)
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    form = CandidateForm
    list_display = ('election', 'full_name', 'department', 'school_level',
                    'matriculation_number', 'candidate_image', 'created_at', 'updated_at')
    list_filter = ('election', 'department', 'school_level')
    search_fields = ('full_name', 'department', 'matriculation_number')

    # Ensure election comes before candidate in list display
    ordering = ('election', 'full_name')
    date_hierarchy = 'created_at'

    readonly_fields = ('created_at', 'updated_at')
    exclude = ('votes_count',)

    # Display candidate image
    def candidate_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    candidate_image.short_description = 'Image'


# Vote Form (Customized for VoteAdmin)
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
    list_display = ('user', 'candidate', 'election', 'voted_at')
    list_filter = ('election', 'voted_at')
    search_fields = ('user__username', 'candidate__full_name',
                     'election__election_type')
    readonly_fields = ('user', 'candidate', 'election', 'voted_at')
    ordering = ('-voted_at',)

    # Disable add, change, and delete permissions
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # Disable saving or editing
    def save_model(self, request, obj, form, change):
        pass  # No saving allowed
