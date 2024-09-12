from django.contrib import admin
from django.utils.html import format_html
from .models import Result, Winner


class WinnerInline(admin.TabularInline):
    model = Winner
    extra = 0  # No extra blank lines in the inline form


# Admin Action for calculating election results
def calculate_election_results(modeladmin, request, queryset):
    for result in queryset:
        result.calculate_results()
        result.calculate_total_votes()
        modeladmin.message_user(
            request, f"Results calculated for {result.election}")


calculate_election_results.short_description = 'Calculate Election Results'


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('election', 'total_votes', 'created_at', 'get_winners')
    readonly_fields = ('total_votes', 'created_at', 'updated_at')
    search_fields = ('election__election_type',)
    ordering = ('-created_at',)
    inlines = [WinnerInline]
    actions = [calculate_election_results]

    # This will display the winners in the admin panel
    def get_winners(self, obj):
        winners = obj.get_winner()
        return format_html('<br>'.join([f"{winner.full_name}" for winner in winners]))
    get_winners.short_description = 'Winners'


@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'result', 'announced_at')
    search_fields = ('candidate__full_name', 'result__election__election_type')
    ordering = ('-announced_at',)
