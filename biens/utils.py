from datetime import datetime
from django.utils import timezone
from .models import Bail, Paiement

def generer_paiements_mensuels():
    aujourd_hui = timezone.now()
    mois_actuel = aujourd_hui.strftime('%B %Y')  # Exemple : "Mai 2025"

    baux_actifs = Bail.objects.filter(date_debut__lte=aujourd_hui, date_fin__gte=aujourd_hui)

    for bail in baux_actifs:
        paiement_existe = Paiement.objects.filter(
            bail=bail,
            locataire=bail.locataire,
            mois_paye=mois_actuel
        ).exists()

        if not paiement_existe:
            Paiement.objects.create(
                bail=bail,
                locataire=bail.locataire,
                mois_paye=mois_actuel,
                montant=bail.montant_loyer
            )
