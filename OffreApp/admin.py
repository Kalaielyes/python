from django.contrib import admin
from .models import Offre


class PrixFilter(admin.SimpleListFilter):
    title = "prix"
    parameter_name = "prix"

    def lookups(self, request, model_admin):
        return [
            ('<100', '< 100'),
            ('<1000', '< 1000'),
            ('<10000', '< 10000'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '<100':
            return queryset.filter(prix__lt=100)
        if self.value() == '<1000':
            return queryset.filter(prix__lt=1000)
        if self.value() == '<10000':
            return queryset.filter(prix__lt=10000)
        return queryset


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('id', 'expedition', 'transporteur', 'vehicule', 'prix', 'delai_jours', 'statut')
    list_filter = (PrixFilter, 'statut', 'transporteur', 'date_proposition')
    search_fields = ('expedition__reference', 'transporteur__raison_sociale', 'vehicule__immatriculation')
    list_editable = ('prix', 'delai_jours', 'statut')
    ordering = ('-date_proposition', '-created_at')
    readonly_fields = ('date_proposition', 'created_at', 'updated_at')

    fieldsets = (
        ("Parties prenantes", {
            'fields': ('expedition', 'transporteur', 'vehicule')
        }),
        ("Conditions de l'offre", {
            'fields': ('prix', 'delai_jours', 'statut')
        }),
        ("Dates & Historique", {
            'fields': ('date_proposition', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
