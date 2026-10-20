from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Entreprise, Utilisateur
from VehiculeApp.models import Vehicule


class VehiculeInline(admin.TabularInline):
    model = Vehicule
    fields = ("immatriculation", "type_vehicule", "capacite_kg", "disponible")
    extra = 2
    show_change_link = True


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    inlines = [VehiculeInline]
    list_display = ('raison_sociale', 'matricule_fiscal', 'type_entreprise', 'gerant', 'created_at')
    list_filter = ('type_entreprise',)
    search_fields = ('raison_sociale', 'matricule_fiscal', 'gerant__username', 'gerant__email')
    list_editable = ('type_entreprise',)
    ordering = ('raison_sociale',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Informations de l'entreprise", {
            'fields': ('raison_sociale', 'matricule_fiscal', 'type_entreprise', 'adresse')
        }),
        ("Gérance", {
            'fields': ('gerant',)
        }),
        ("Dates & Historique", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('user_id', 'username', 'email', 'role', 'telephone', 'is_active', 'created_at')
    list_filter = ('role', 'is_active')
    search_fields = ('user_id', 'username', 'email', 'telephone')
    list_editable = ('role', 'telephone')
    ordering = ('user_id',)
    readonly_fields = ('user_id', 'date_joined', 'last_login', 'created_at', 'updated_at')

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

    # Formulaire de création : champs différents (pas de
    # user_id ni d'historique, mais password1/password2).
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "usable_password",
                    "password1",
                    "password2",
                    "email",
                    "telephone",
                    "role",
                ),
            },
        ),
    )
