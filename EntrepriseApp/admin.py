from django.contrib import admin
from .models import Entreprise, Utilisateur
from django.contrib.auth.admin import UserAdmin
from VehiculeApp.models import Vehicule


# Register your models here.
admin.site.site_header = 'TransConnect - Administration'
admin.site.site_title = 'TransConnect'
admin.site.index_title = "Tableau de bord"




@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
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


    #formulaire de création : champs différents (pas de user_id ni d'historique, mais passw1/passw2)
    add_fields = (
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
                )
            }
        )
    )
    list_filter = ("role", "is_active")




class VehiculeInline(admin.TabularInline):
    model = Vehicule
    fields = ("immatricule", "type_vehicule", "capacite_kg", "disponible")
    extra = 2
    show_change_link = True


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    inlines = [VehiculeInline]
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

#admin.site.register(Expedition, ExpeditionAdmin)