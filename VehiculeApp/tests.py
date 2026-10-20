from django.test import TestCase
from django.core.exceptions import ValidationError
from EntrepriseApp.models import Utilisateur, Entreprise
from .models import Vehicule


class VehiculeModelTest(TestCase):
    def setUp(self):
        self.user_trans = Utilisateur.objects.create(
            username='transp_user',
            email='transp@gmail.com',
            role='transporteur'
        )
        self.transp = Entreprise.objects.create(
            raison_sociale='Société Express Transport',
            matricule_fiscal='1234567AAM000',
            type_entreprise='transporteur',
            adresse='Avenue Habib Bourguiba Tunis 1001',
            gerant=self.user_trans
        )
        self.user_charg = Utilisateur.objects.create(
            username='charg_user',
            email='charg@gmail.com',
            role='chargeur'
        )
        self.charg = Entreprise.objects.create(
            raison_sociale='Société Commerciale SARL',
            matricule_fiscal='9876543BBM000',
            type_entreprise='chargeur',
            adresse='Route de la Marsa km 10 Tunis',
            gerant=self.user_charg
        )

    def test_vehicule_creation_transporteur_success(self):
        v = Vehicule.objects.create(
            immatriculation='123TU4567',
            type_vehicule='camionnette',
            capacite_kg=1200,
            disponible=True,
            entreprise=self.transp
        )
        self.assertEqual(v.immatriculation, '123TU4567')
        self.assertEqual(v.immatricule, '123TU4567')

    def test_vehicule_entreprise_must_be_transporteur(self):
        v = Vehicule(
            immatriculation='999TU9999',
            type_vehicule='fourgon',
            capacite_kg=3000,
            disponible=True,
            entreprise=self.charg  # Chargeur instead of transporteur
        )
        with self.assertRaises(ValidationError):
            v.full_clean()

    def test_capacite_kg_cannot_be_zero(self):
        v = Vehicule(
            immatriculation='888TU8888',
            type_vehicule='fourgon',
            capacite_kg=0,  # Zero capacity
            disponible=True,
            entreprise=self.transp
        )
        with self.assertRaises(ValidationError):
            v.full_clean()
