from django.contrib import admin
from .models import Vehicule


@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('immatriculation', 'type_vehicule', 'disponible', 'capacite_kg', 'entreprise')
    list_filter = ('disponible', 'type_vehicule', 'entreprise')
    search_fields = ('immatriculation', 'type_vehicule', 'entreprise__raison_sociale')
    list_editable = ('type_vehicule', 'disponible', 'capacite_kg')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Informations générales", {
            'fields': ('immatriculation', 'type_vehicule', 'capacite_kg', 'disponible')
        }),
        ("Entreprise associée", {
            'fields': ('entreprise',)
        }),
        ("Dates & Historique", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
