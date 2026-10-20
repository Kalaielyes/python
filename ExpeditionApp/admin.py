from django.contrib import admin
from django.utils import timezone
from .models import Expedition


class EnRetardFilter(admin.SimpleListFilter):
    title = "en retard"
    parameter_name = "en_retard"

    def lookups(self, request, model_admin):
        return [("oui", "Oui"), ("non", "Non")]

    def queryset(self, request, queryset):
        aujourd_hui = timezone.now().date()
        if self.value() == "oui":
            return queryset.filter(statut="publiee", date_souhaitee__lt=aujourd_hui)
        if self.value() == "non":
            return queryset.exclude(statut="publiee", date_souhaitee__lt=aujourd_hui)
        return queryset


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('reference', 'entreprise', 'ville_depart', 'ville_arrivee', 'poids_kg', 'date_souhaitee', 'statut')
    list_filter = (EnRetardFilter, 'statut', 'date_souhaitee', 'entreprise')
    search_fields = ('reference', 'ville_depart', 'ville_arrivee', 'entreprise__raison_sociale')
    list_editable = ('statut',)
    ordering = ('-created_at',)
    readonly_fields = ('reference', 'created_at', 'updated_at')

    fieldsets = (
        ("Informations générales", {
            'fields': ('reference', 'entreprise', 'statut')
        }),
        ("Détails logistiques", {
            'fields': ('ville_depart', 'ville_arrivee', 'poids_kg', 'date_souhaitee', 'description')
        }),
        ("Dates & Historique", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
