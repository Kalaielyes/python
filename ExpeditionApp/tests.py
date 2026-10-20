from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from EntrepriseApp.models import Utilisateur, Entreprise
from .models import Expedition


class ExpeditionModelTest(TestCase):
    def setUp(self):
        self.user_charg = Utilisateur.objects.create(
            username='user_exp_charg',
            email='exp_charg@gmail.com',
            role='chargeur'
        )
        self.charg = Entreprise.objects.create(
            raison_sociale='Société Négoce et Commerce',
            matricule_fiscal='1122334AAM000',
            type_entreprise='chargeur',
            adresse='Zone Portuaire de Rades Tunis',
            gerant=self.user_charg
        )
        self.user_trans = Utilisateur.objects.create(
            username='user_exp_trans',
            email='exp_trans@gmail.com',
            role='transporteur'
        )
        self.transp = Entreprise.objects.create(
            raison_sociale='Société Flotte Rapide Express',
            matricule_fiscal='2233445BBM000',
            type_entreprise='transporteur',
            adresse='Route de Bizerte km 5 Tunis',
            gerant=self.user_trans
        )

    def test_reference_auto_generation(self):
        exp1 = Expedition.objects.create(
            ville_depart='Tunis',
            ville_arrivee='Sousse',
            poids_kg=Decimal('500.00'),
            date_souhaitee=timezone.now().date(),
            entreprise=self.charg
        )
        annee = timezone.now().strftime('%y')
        self.assertEqual(exp1.reference, f"EXP-{annee}-00001")

        exp2 = Expedition.objects.create(
            ville_depart='Sfax',
            ville_arrivee='Gabès',
            poids_kg=Decimal('1200.50'),
            date_souhaitee=timezone.now().date(),
            entreprise=self.charg
        )
        self.assertEqual(exp2.reference, f"EXP-{annee}-00002")

    def test_expedition_entreprise_must_be_chargeur(self):
        exp = Expedition(
            ville_depart='Tunis',
            ville_arrivee='Bizerte',
            poids_kg=Decimal('300.00'),
            date_souhaitee=timezone.now().date(),
            entreprise=self.transp  # transporteur instead of chargeur
        )
        with self.assertRaises(ValidationError):
            exp.full_clean()

    def test_poids_kg_cannot_be_zero(self):
        exp = Expedition(
            ville_depart='Tunis',
            ville_arrivee='Nabeul',
            poids_kg=Decimal('0.00'),
            date_souhaitee=timezone.now().date(),
            entreprise=self.charg
        )
        with self.assertRaises(ValidationError):
            exp.full_clean()
