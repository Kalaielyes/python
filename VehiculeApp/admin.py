from django.contrib import admin
from .models import Vehicule

# Register your models here.

@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('immatricule', 'type_vehicule', 'disponible', 'capacite_kg', 'entreprise')
    list_filter = ('disponible', 'type_vehicule', 'entreprise')
    search_fields = ('immatricule', 'type_vehicule', 'entreprise__raison_social')
    list_editable = ('type_vehicule', 'disponible', 'capacite_kg')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Informations generales", {
            'fields': ('immatricule', 'type_vehicule', 'capacite_kg', 'disponible')
        }),
        ("Entreprise associee", {
            'fields': ('entreprise',)
        }),
        ("Dates & Historique", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
