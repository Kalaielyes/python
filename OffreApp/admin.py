from django.contrib import admin
from .models import Offre

# Register your models here.


class Prix(admin.SimpleListFilter):
    title = 'prix'
    parameter_name = 'prix'

    def lookups(self, request, model_admin):
        return [
            ('moins_100', 'Moins de 100'),
            ('100_1000', 'Entre 100 et 1000'),
            ('1000_10000', 'Entre 1000 et 10000'),
            ('plus_10000', 'Plus de 10000'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'moins_100':
            return queryset.filter(prix__lt=100)
        elif self.value() == '100_1000':
            return queryset.filter(prix__gte=100, prix__lte=1000)
        elif self.value() == '1000_10000':
            return queryset.filter(prix__gte=1000, prix__lte=10000)
        elif self.value() == 'plus_10000':
            return queryset.filter(prix__gt=10000)
        return queryset
        

@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('id', 'expedition', 'transporteur', 'vehicule', 'prix', 'delai_jours', 'statut')
    list_filter = ('statut', 'transporteur', 'date_proposition', Prix)
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

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('prix', 'delai_jours', 'status', 'Entreprise', 'Vehicule', 'expedition')
        }),
    )