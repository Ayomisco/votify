from elections.models import Candidate
from django.contrib import admin
from django import forms
from django.utils import timezone
from .models import Winner, Result
from elections.models import Candidate, Vote
from .forms import WinnerForm

def calculate_election_results(modeladmin, request, queryset):
    for result in queryset:
        result.calculate_results()
        result.calculate_total_votes()
        modeladmin.message_user(
            request, f"Results calculated for {result.election}")


calculate_election_results.short_description = 'Calculate Election Results'


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('election', 'total_votes', 'created_at',
                    'get_announced_at', 'get_winners')
    readonly_fields = ('total_votes', 'created_at', 'updated_at')
    search_fields = ('election__election_type',)
    ordering = ('-created_at',)  # Ordering by created_at
    actions = [calculate_election_results, 'make_public']

    def get_announced_at(self, obj):
        return obj.announced_at
    get_announced_at.short_description = 'Announced At'

    def get_winners(self, obj):
        winners = obj.get_winner()
        return format_html('<br>'.join([f"{winner.candidate.full_name}" for winner in winners]))
    get_winners.short_description = 'Winners'

    def make_public(self, request, queryset):
        # Add logic to make the results public
        updated_count = queryset.update(is_public=True)
        self.message_user(
            request, f"{updated_count} results marked as public.")
    make_public.short_description = 'Make Results Public'


class WinnerAdmin(admin.ModelAdmin):
    form = WinnerForm
    list_display = ('candidate', 'result', 'announced_at')
    search_fields = ('candidate__full_name', 'result__election__election_type')
    ordering = ('-announced_at',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            # Make candidate field read-only and result field disabled if editing
            return self.readonly_fields + ('candidate', 'result')
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Automatically set the announcement time if it's not yet announced
            obj.announced_at = timezone.now() if obj.announced_at is None else obj.announced_at
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            # Disable result field if editing
            form.base_fields['result'].disabled = True
        return form

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if obj and obj.announced_at:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Winner, WinnerAdmin)
