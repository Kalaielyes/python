from django.contrib import admin
from .models import Offre

# Register your models here.

class OffreAdmin(admin.ModelAdmin):
    list_display = ('id', 'expedition', 'transporteur', 'vehicule', 'prix', 'delai_jours', 'statut')
    list_filter = ('statut', 'transporteur', 'date_proposition')
    search_fields = ('expedition__reference', 'transporteur__raison_social', 'vehicule__immatricule')
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

admin.site.register(Offre, OffreAdmin)