from django.contrib import admin
from .models import Offre


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'expedition',
        'transporteur',
        'prix',
        'delai_jours',
        'statut',
        'date_proposition',
    )
    list_filter = ('statut', 'date_proposition', 'transporteur')
    search_fields = ('expedition__reference', 'transporteur__raison_sociale')
    readonly_fields = ('date_proposition', 'created_at', 'updated_at')
    date_hierarchy = 'date_proposition'

    fieldsets = (
        ('Détails de l\'offre', {
            'fields': ('prix', 'delai_jours', 'statut')
        }),
        ('Relations', {
            'fields': ('expedition', 'transporteur', 'vehicule')
        }),
        ('Horodatage', {
            'fields': ('date_proposition', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )