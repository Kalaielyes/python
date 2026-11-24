from django.contrib import admin
from .models import Entreprise, Utilisateur

# Register your models here.

class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('raison_social', 'matricule_fiscal', 'type_entreprise', 'gerant')
    list_filter = ('type_entreprise',)
    search_fields = ('raison_social', 'matricule_fiscal', 'gerant__username')
    list_editable = ('type_entreprise',)
    ordering = ('raison_social',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Informations de l'entreprise", {
            'fields': ('raison_social', 'matricule_fiscal', 'type_entreprise', 'adresse')
        }),
        ("Gérance", {
            'fields': ('gerant',)
        }),
        ("Dates & Historique", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'role', 'telephone', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('user_id', 'username', 'email', 'telephone')
    list_editable = ('role', 'telephone')
    ordering = ('user_id',)
    readonly_fields = ('user_id', 'created_at', 'updated_at')

    fieldsets = (
        ("Informations personnelles & Compte", {
            'fields': ('user_id', 'username', 'email', 'role', 'telephone')
        }),
        ("Permissions & Statut", {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
            'classes': ('collapse',),
        }),
        ("Dates & Historique", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


admin.site.register(Entreprise, EntrepriseAdmin)
admin.site.register(Utilisateur, UtilisateurAdmin)