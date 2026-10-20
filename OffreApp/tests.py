from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from EntrepriseApp.models import Utilisateur, Entreprise
from VehiculeApp.models import Vehicule
from ExpeditionApp.models import Expedition
from .models import Offre


class OffreModelBusinessRulesTest(TestCase):
    def setUp(self):
        # Chargeur
        self.user_charg = Utilisateur.objects.create_user(
            username='user_ch_test',
            email='user_ch@gmail.com',
            password='password123',
            role='chargeur'
        )
        self.charg = Entreprise.objects.create(
            raison_sociale='Agro Alimentaire Tunisie SARL',
            matricule_fiscal='1234567AAM000',
            type_entreprise='chargeur',
            adresse='Route de Mornag km 4 Tunis 2000',
            gerant=self.user_charg
        )

        # Transporteur 1
        self.user_trans1 = Utilisateur.objects.create_user(
            username='user_tr1_test',
            email='user_tr1@gmail.com',
            password='password123',
            role='transporteur'
        )
        self.trans1 = Entreprise.objects.create(
            raison_sociale='Société Express Transport 1',
            matricule_fiscal='2345678BBM000',
            type_entreprise='transporteur',
            adresse='Avenue Habib Bourguiba Tunis 1000',
            gerant=self.user_trans1
        )

        # Transporteur 2
        self.user_trans2 = Utilisateur.objects.create_user(
            username='user_tr2_test',
            email='user_tr2@gmail.com',
            password='password123',
            role='transporteur'
        )
        self.trans2 = Entreprise.objects.create(
            raison_sociale='Société Rapide Fret SARL 2',
            matricule_fiscal='3456789CAM000',
            type_entreprise='transporteur',
            adresse='Boulevard du 14 Janvier Sousse 4000',
            gerant=self.user_trans2
        )

        # Véhicules
        self.vehicule_t1 = Vehicule.objects.create(
            immatriculation='100TU1000',
            type_vehicule='fourgon',
            capacite_kg=3000,
            disponible=True,
            entreprise=self.trans1
        )
        self.vehicule_t2 = Vehicule.objects.create(
            immatriculation='200TU2000',
            type_vehicule='fourgon',
            capacite_kg=3000,
            disponible=True,
            entreprise=self.trans2
        )

        # Expédition publiée
        self.expedition = Expedition.objects.create(
            ville_depart='Tunis',
            ville_arrivee='Sfax',
            poids_kg=Decimal('1000.00'),
            date_souhaitee=timezone.now().date(),
            statut='publiee',
            entreprise=self.charg
        )

    def test_regle_1_transporteur_only(self):
        """R1: Une offre ne peut être créée que par une entreprise dont type_entreprise = transporteur."""
        offre = Offre(
            prix=Decimal('500.00'),
            delai_jours=2,
            expedition=self.expedition,
            transporteur=self.charg,  # Entreprise chargeur !
            vehicule=self.vehicule_t1
        )
        with self.assertRaises(ValidationError):
            offre.full_clean()

    def test_regle_2_vehicule_same_enterprise(self):
        """R2: Le véhicule associé à une offre doit appartenir à la même entreprise que le transporteur de l'offre."""
        offre = Offre(
            prix=Decimal('600.00'),
            delai_jours=2,
            expedition=self.expedition,
            transporteur=self.trans1,
            vehicule=self.vehicule_t2  # Véhicule appartient à trans2 !
        )
        with self.assertRaises(ValidationError):
            offre.full_clean()

    def test_regle_3_expedition_must_be_publiee(self):
        """R3: Une expédition ne peut recevoir de nouvelles offres que si son statut est publiee."""
        self.expedition.statut = 'attribuee'
        self.expedition.save()

        offre = Offre(
            prix=Decimal('700.00'),
            delai_jours=3,
            expedition=self.expedition,
            transporteur=self.trans1,
            vehicule=self.vehicule_t1
        )
        with self.assertRaises(ValidationError):
            offre.full_clean()

    def test_regle_4_no_duplicate_active_proposee_offers(self):
        """R4: Une entreprise ne peut pas avoir deux offres au statut proposee actives simultanément sur la même expédition."""
        Offre.objects.create(
            prix=Decimal('500.00'),
            delai_jours=2,
            statut='proposee',
            expedition=self.expedition,
            transporteur=self.trans1,
            vehicule=self.vehicule_t1
        )

        offre_doublon = Offre(
            prix=Decimal('450.00'),
            delai_jours=1,
            statut='proposee',
            expedition=self.expedition,
            transporteur=self.trans1,
            vehicule=self.vehicule_t1
        )
        with self.assertRaises(ValidationError):
            offre_doublon.full_clean()

    def test_regle_5_cascade_on_acceptance(self):
        """R5: Cascade à l'acceptation : offre passe à acceptee -> expédition passe à attribuee, autres offres deviennent refusee."""
        offre1 = Offre.objects.create(
            prix=Decimal('500.00'),
            delai_jours=2,
            statut='proposee',
            expedition=self.expedition,
            transporteur=self.trans1,
            vehicule=self.vehicule_t1
        )
        offre2 = Offre.objects.create(
            prix=Decimal('550.00'),
            delai_jours=3,
            statut='proposee',
            expedition=self.expedition,
            transporteur=self.trans2,
            vehicule=self.vehicule_t2
        )

        # Accepter offre1
        offre1.statut = 'acceptee'
        offre1.save()

        # Vérifier cascade
        self.expedition.refresh_from_db()
        offre2.refresh_from_db()

        self.assertEqual(self.expedition.statut, 'attribuee')
        self.assertEqual(offre2.statut, 'refusee')

    def test_regle_6_indisponible_vehicule_rejected(self):
        """R6: Un véhicule dont disponible = False ne peut pas être proposé sur une nouvelle offre."""
        self.vehicule_t1.disponible = False
        self.vehicule_t1.save()

        offre = Offre(
            prix=Decimal('800.00'),
            delai_jours=2,
            expedition=self.expedition,
            transporteur=self.trans1,
            vehicule=self.vehicule_t1
        )
        with self.assertRaises(ValidationError):
            offre.full_clean()

    def test_regle_7_vehicule_type_weight_compatibility(self):
        """R7: L'attribut type_vehicule conditionne la compatibilité avec le poids d'une expédition."""
        # Camionnette : max ~1.5t (1500 kg)
        vehicule_camionnette = Vehicule.objects.create(
            immatriculation='300TU3000',
            type_vehicule='camionnette',
            capacite_kg=1500,
            disponible=True,
            entreprise=self.trans1
        )
        # Expédition trop lourde pour camionnette (2000 kg > 1500 kg)
        exp_lourde = Expedition.objects.create(
            ville_depart='Tunis',
            ville_arrivee='Sousse',
            poids_kg=Decimal('2000.00'),
            date_souhaitee=timezone.now().date(),
            statut='publiee',
            entreprise=self.charg
        )

        offre = Offre(
            prix=Decimal('900.00'),
            delai_jours=1,
            expedition=exp_lourde,
            transporteur=self.trans1,
            vehicule=vehicule_camionnette
        )
        with self.assertRaises(ValidationError):
            offre.full_clean()


from django.test import RequestFactory
from django.contrib.admin.sites import site
from .admin import PrixFilter, OffreAdmin


class PrixFilterTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        user_ch = Utilisateur.objects.create_user(username='ch_flt', email='ch_flt@gmail.com', password='123')
        ch = Entreprise.objects.create(
            raison_sociale='Chargeur Filter SA',
            matricule_fiscal='5555555AAM000',
            type_entreprise='chargeur',
            adresse='123 Rue de la Liberté Tunis 1000',
            gerant=user_ch
        )
        user_tr = Utilisateur.objects.create_user(username='tr_flt', email='tr_flt@gmail.com', password='123')
        tr = Entreprise.objects.create(
            raison_sociale='Transport Filter SA',
            matricule_fiscal='6666666BBM000',
            type_entreprise='transporteur',
            adresse='456 Route de Sfax Km 2 Tunis 1000',
            gerant=user_tr
        )
        veh = Vehicule.objects.create(
            immatriculation='777TU7777',
            type_vehicule='semi_remorque',
            capacite_kg=25000,
            disponible=True,
            entreprise=tr
        )
        exp = Expedition.objects.create(
            ville_depart='Tunis',
            ville_arrivee='Sousse',
            poids_kg=Decimal('500.00'),
            date_souhaitee=timezone.now().date(),
            statut='publiee',
            entreprise=ch
        )

        self.o1 = Offre.objects.create(prix=Decimal('50.00'), delai_jours=1, statut='proposee', expedition=exp, transporteur=tr, vehicule=veh)
        # Change status or use another expedition to create more offers
        exp2 = Expedition.objects.create(ville_depart='Tunis', ville_arrivee='Sfax', poids_kg=Decimal('500.00'), date_souhaitee=timezone.now().date(), statut='publiee', entreprise=ch)
        self.o2 = Offre.objects.create(prix=Decimal('500.00'), delai_jours=1, statut='proposee', expedition=exp2, transporteur=tr, vehicule=veh)
        exp3 = Expedition.objects.create(ville_depart='Tunis', ville_arrivee='Gabes', poids_kg=Decimal('500.00'), date_souhaitee=timezone.now().date(), statut='publiee', entreprise=ch)
        self.o3 = Offre.objects.create(prix=Decimal('5000.00'), delai_jours=1, statut='proposee', expedition=exp3, transporteur=tr, vehicule=veh)

    def test_prix_filter_cases(self):
        model_admin = OffreAdmin(Offre, site)

        # Case < 100
        request_lt100 = self.factory.get('/admin/OffreApp/offre/?prix=%3C100')
        filter_lt100 = PrixFilter(request_lt100, request_lt100.GET.copy(), Offre, model_admin)
        qs_lt100 = filter_lt100.queryset(request_lt100, Offre.objects.all())
        self.assertIn(self.o1, qs_lt100)
        self.assertNotIn(self.o2, qs_lt100)
        self.assertNotIn(self.o3, qs_lt100)

        # Case < 1000
        request_lt1000 = self.factory.get('/admin/OffreApp/offre/?prix=%3C1000')
        filter_lt1000 = PrixFilter(request_lt1000, request_lt1000.GET.copy(), Offre, model_admin)
        qs_lt1000 = filter_lt1000.queryset(request_lt1000, Offre.objects.all())
        self.assertIn(self.o1, qs_lt1000)
        self.assertIn(self.o2, qs_lt1000)
        self.assertNotIn(self.o3, qs_lt1000)

        # Case < 10000
        request_lt10000 = self.factory.get('/admin/OffreApp/offre/?prix=%3C10000')
        filter_lt10000 = PrixFilter(request_lt10000, request_lt10000.GET.copy(), Offre, model_admin)
        qs_lt10000 = filter_lt10000.queryset(request_lt10000, Offre.objects.all())
        self.assertIn(self.o1, qs_lt10000)
        self.assertIn(self.o2, qs_lt10000)
        self.assertIn(self.o3, qs_lt10000)
