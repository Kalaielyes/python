from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Entreprise


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('user_id', 'username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('user_id', 'username', 'email')

    fieldsets = UserAdmin.fieldsets + (
        ('Informations TransConnect', {
            'fields': ('user_id', 'telephone', 'role'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations TransConnect', {
            'fields': ('email', 'telephone', 'role'),
        }),
    )


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('raison_sociale', 'matricule_fiscal', 'type_entreprise', 'utilisateur', 'created_at')
    list_filter = ('type_entreprise',)
    search_fields = ('raison_sociale', 'matricule_fiscal')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Informations générales', {
            'fields': ('raison_sociale', 'matricule_fiscal', 'type_entreprise')
        }),
        ('Contact et rattachement', {
            'fields': ('adresse', 'utilisateur')
        }),
        ('Horodatage', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )