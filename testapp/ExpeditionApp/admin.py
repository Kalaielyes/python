from django.contrib import admin
from .models import Expedition

# Register your models here.

class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('reference', 'entreprise', 'ville_depart', 'ville_arrivee', 'poids_kg', 'date_souhaitee', 'statut')
    list_filter = ('statut', 'date_souhaitee', 'entreprise')
    search_fields = ('reference', 'ville_depart', 'ville_arrivee', 'entreprise__raison_social')
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

admin.site.register(Expedition, ExpeditionAdmin)