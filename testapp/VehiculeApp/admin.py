from django.contrib import admin
from .models import Vehicule

# Register your models here.

class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('immatricule', 'type_vehicule', 'disponible', 'capacite_kg', 'entreprise')
    list_filter = ('disponible', 'type_vehicule', 'entreprise')
    search_fields = ('immatricule', 'type_vehicule', 'entreprise__raison_social')
    list_editable = ('type_vehicule', 'disponible', 'capacite_kg')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Informations générales", {
            'fields': ('immatricule', 'type_vehicule', 'capacite_kg', 'disponible')
        }),
        ("Entreprise associée", {
            'fields': ('entreprise',)
        }),
        ("Dates & Historique", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(Vehicule, VehiculeAdmin)