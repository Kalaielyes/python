from django.contrib import admin
from .models import Expedition


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = (
        'reference',
        'ville_depart',
        'ville_arrivee',
        'poids_kg',
        'statut',
        'entreprise',
        'created_at',
    )
    list_filter = ('statut', 'date_souhaitee', 'entreprise')
    search_fields = ('reference', 'ville_depart', 'ville_arrivee', 'description')
    readonly_fields = ('reference', 'created_at', 'updated_at')
    date_hierarchy = 'date_souhaitee'          # navigation par date en haut

    fieldsets = (
        ('Référence', {
            'fields': ('reference',)
        }),
        ('Trajet et détails', {
            'fields': ('ville_depart', 'ville_arrivee', 'poids_kg', 'date_souhaitee', 'description')
        }),
        ('Statut et rattachement', {
            'fields': ('statut', 'entreprise')
        }),
        ('Horodatage', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )