from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Utilisateur, Entreprise


class UtilisateurModelTest(TestCase):
    def test_user_id_auto_generation_format(self):
        user1 = Utilisateur.objects.create_user(
            username='user1',
            email='user1@gmail.com',
            password='password123'
        )
        annee = timezone.now().strftime('%y')
        self.assertEqual(user1.user_id, f"{annee}user00")

        user2 = Utilisateur.objects.create_user(
            username='user2',
            email='user2@gmail.com',
            password='password123'
        )
        self.assertEqual(user2.user_id, f"{annee}user01")

    def test_email_gmail_domain_accepted(self):
        user = Utilisateur.objects.create_user(
            username='validgmail',
            email='valid.person@gmail.com',
            password='password123'
        )
        user.full_clean()
        self.assertTrue(user.user_id)

    def test_email_non_gmail_rejected(self):
        user = Utilisateur(
            username='invalidemail',
            email='invalid@yahoo.com'
        )
        with self.assertRaises(ValidationError):
            user.full_clean()


class EntrepriseModelTest(TestCase):
    def setUp(self):
        self.user_chargeur = Utilisateur.objects.create_user(
            username='user_ch',
            email='user_ch@gmail.com',
            password='password123',
            role='chargeur'
        )
        self.user_transporteur = Utilisateur.objects.create_user(
            username='user_tr',
            email='user_tr@gmail.com',
            password='password123',
            role='transporteur'
        )

    def test_matricule_fiscal_valid_formats(self):
        formats = [
            '1234567AAM000',
            '1234567/A/A/M/000',
            '1234567-A-A-M-000',
            '1234567/b/b/p/001'
        ]
        for i, mf in enumerate(formats):
            user = Utilisateur.objects.create_user(
                username=f'user_test_{i}',
                email=f'user_test_{i}@gmail.com',
                password='password123'
            )
            ent = Entreprise(
                raison_sociale=f'Entreprise {i}',
                matricule_fiscal=mf,
                type_entreprise='chargeur',
                adresse='123 Rue de la République Tunis 1000',
                gerant=user
            )
            # Should pass full_clean
            ent.full_clean()
            ent.save()

    def test_matricule_fiscal_invalid_format(self):
        ent = Entreprise(
            raison_sociale='Entreprise Invalide',
            matricule_fiscal='123456AAM000',  # Only 6 digits instead of 7
            type_entreprise='chargeur',
            adresse='123 Rue de la République Tunis 1000',
            gerant=self.user_chargeur
        )
        with self.assertRaises(ValidationError):
            ent.full_clean()

    def test_adresse_min_length_validation(self):
        ent = Entreprise(
            raison_sociale='Entreprise Courte Adresse',
            matricule_fiscal='1234567AAM000',
            type_entreprise='chargeur',
            adresse='Trop court',  # Less than 20 chars
            gerant=self.user_chargeur
        )
        with self.assertRaises(ValidationError):
            ent.full_clean()

    def test_compatibility_properties(self):
        ent = Entreprise.objects.create(
            raison_sociale='TransLogistics SARL',
            matricule_fiscal='7654321BBM000',
            type_entreprise='transporteur',
            adresse='Zone Industrielle Ben Arous Tunisie',
            gerant=self.user_transporteur
        )
        # raison_social property
        self.assertEqual(ent.raison_social, 'TransLogistics SARL')
        # utilisateur property
        self.assertEqual(ent.utilisateur, self.user_transporteur)
