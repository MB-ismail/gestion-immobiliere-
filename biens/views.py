from django.shortcuts import render, get_object_or_404, redirect
from .models import Bien
from .models import DemandeBail
from .forms import BienForm

from django.contrib.auth.decorators import login_required, user_passes_test

#  Lister les biens
@login_required
def list_biens(request):
    biens = Bien.objects.all()
    return render(request, 'biens/list_biens.html', {'biens': biens})

#  Voir le détail d’un bien
def bien_detail(request, pk):
    bien = get_object_or_404(Bien, pk=pk)
    return render(request, 'biens/bien_detail.html', {'bien': bien})

#  Ajouter un bien
#  1. La fonction de test 
def est_proprietaire(user):
    return user.is_authenticated and user.role == 'proprietaire'


@login_required
@user_passes_test(est_proprietaire)
def ajouter_bien(request):
    if request.method == 'POST':
        form = BienForm(request.POST, request.FILES)
        if form.is_valid():
            bien = form.save(commit=False)
            bien.proprietaire = request.user
            bien.save()
            return redirect('list_biens')
    else:
        form = BienForm()
    return render(request, 'biens/bien_form.html', {'form': form})

#  Modifier un bien
@login_required
def modifier_bien(request, pk):
    bien = get_object_or_404(Bien, pk=pk)
    if request.method == 'POST':
        form = BienForm(request.POST, request.FILES, instance=bien)
        if form.is_valid():
            form.save()
            return redirect('list_biens')
    else:
        form = BienForm(instance=bien)
    return render(request, 'biens/bien_form.html', {'form': form})

#  Supprimer un bien
@login_required
def supprimer_bien(request, pk):
    bien = get_object_or_404(Bien, pk=pk)
    if request.method == 'POST':
        bien.delete()
        return redirect('list_biens')
    return render(request, 'biens/bien_confirm_delete.html', {'bien': bien})

from .models import Bail
from .forms import BailForm

@login_required
def list_bails(request):
    baux = Bail.objects.all()
    return render(request, 'biens/list_bails.html', {'baux': baux})

from .models import Bien, Bail, CustomUser
from .forms import BailForm

@login_required
@user_passes_test(est_proprietaire)
def ajouter_bail(request, bien_id=None, locataire_id=None):
    initial_data = {}
    if bien_id:
        initial_data['bien'] = get_object_or_404(Bien, id=bien_id)
    if locataire_id:
        initial_data['locataire'] = get_object_or_404(CustomUser, id=locataire_id)

    if request.method == 'POST':
        form = BailForm(request.POST, initial=initial_data)
        if form.is_valid():
            bail = form.save(commit=False)
            bail.est_valide_proprio = True  # Le propriétaire a initié
            bail.save()
            return redirect('list_bails')
    else:
        form = BailForm(initial=initial_data)

    return render(request, 'biens/bail_form.html', {'form': form})

@login_required
def supprimer_bail(request, pk):
    bail = get_object_or_404(Bail, pk=pk)
    bien = bail.bien
    if request.method == 'POST':
        bail.delete()
        if not Bail.objects.filter(bien=bien).exists():
            bien.statut = 'libre'
            bien.save()
        return redirect('list_bails')
    return render(request, 'biens/bail_confirm_delete.html', {'bail': bail})

def est_locataire(user):
    return user.is_authenticated and user.role == 'locataire'

@login_required
@user_passes_test(est_locataire)
def demander_bail(request, bien_id):
    bien = get_object_or_404(Bien, id=bien_id)

    if request.method == 'POST':
        message = request.POST.get('message', '')
        DemandeBail.objects.create(
            bien=bien,
            locataire=request.user,
            message=message
        )
        return redirect('biens_disponibles')  # à adapter à ta vue publique
    return render(request, 'biens/demande_bail.html', {'bien': bien})

@login_required
@user_passes_test(est_proprietaire)
def demandes_recuees(request):
    demandes = DemandeBail.objects.filter(bien__proprietaire=request.user, statut='en attente')
    return render(request, 'biens/demandes_recuees.html', {'demandes': demandes})

from datetime import timedelta
from django.utils import timezone
from .models import Bail

@login_required
@user_passes_test(est_proprietaire)
def accepter_demande(request, demande_id):
    demande = get_object_or_404(DemandeBail, pk=demande_id, bien__proprietaire=request.user)

    # Mise à jour du statut
    demande.statut = 'accepte'
    demande.save()

    # Création du bail
    Bail.objects.create(
        bien=demande.bien,
        locataire=demande.locataire,
        date_debut=timezone.now(),
        date_fin=timezone.now() + timedelta(days=365),
        montant_loyer=demande.bien.prix
    )

    # Mise à jour du bien comme loué
    demande.bien.statut = 'loue'
    demande.bien.save()

    return redirect('demandes_recuees')

@login_required
@user_passes_test(est_proprietaire)
def refuser_demande(request, demande_id):
    demande = get_object_or_404(DemandeBail, pk=demande_id, bien__proprietaire=request.user)
    demande.statut = 'refuse'
    demande.save()
    return redirect('demandes_recuees')

from django.db.models import Q

def biens_disponibles(request):
    biens = Bien.objects.filter(statut='libre')
    return render(request, 'biens/biens_disponibles.html', {'biens': biens})

@login_required
@user_passes_test(est_locataire)
def mes_demandes_bail(request):
    demandes = DemandeBail.objects.filter(locataire=request.user).select_related('bien').order_by('-date_demande')
    return render(request, 'biens/mes_demandes_bail.html', {'demandes': demandes})

from django.http import HttpResponseForbidden
from .models import Bail

@login_required
@user_passes_test(est_locataire)
def detail_bail(request, bail_id):
    bail = get_object_or_404(Bail, id=bail_id)

    # Vérification que seul le propriétaire ou le locataire peut voir le bail
    if request.user != bail.locataire and request.user != bail.bien.proprietaire:
        return HttpResponseForbidden("Vous n'avez pas accès à ce contrat.")

    if request.method == 'POST':
        # Validation côté propriétaire
        if 'valider_proprio' in request.POST and request.user == bail.bien.proprietaire:
            bail.est_valide_proprio = True
            bail.save()
        # Validation côté locataire
        elif 'valider_locataire' in request.POST and request.user == bail.locataire:
            bail.est_valide_locataire = True
            bail.save()

    return render(request, 'biens/detail_bail.html', {'bail': bail})

def est_locataire(user):
    return user.is_authenticated and user.role == 'locataire'

@login_required
@user_passes_test(est_locataire)
def mes_baux(request):
    baux = Bail.objects.filter(locataire=request.user).select_related('bien')
    return render(request, 'biens/mes_baux.html', {'baux': baux}) 

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from io import BytesIO
from .models import Bail

from num2words import num2words

def contrat_pdf_xhtml(request, pk):
    bail = Bail.objects.get(pk=pk)
    montant_lettres = num2words(bail.montant_loyer, lang='fr')
    garantie_lettres = num2words(bail.garantie, lang='fr')

    template = get_template('biens/contrat_pdf.html')
    html = template.render({
        'bail': bail,
        'montant_lettres': montant_lettres,
        'garantie_lettres': garantie_lettres,
        'lieu_signature': 'Casablanca',  # optionnel si tu veux passer ça manuellement
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="contrat_bail_{bail.id}.pdf"'

    valide = bail.est_valide_proprio and bail.est_valide_locataire
    
    result = BytesIO()
    pisa.CreatePDF(html, dest=result)
    response.write(result.getvalue())
    return response

@login_required
def valider_bail_proprio(request, pk):
    bail = get_object_or_404(Bail, id=pk)
    if request.user == bail.bien.proprietaire:
        bail.est_valide_proprio = True
        bail.save()
    return redirect('detail_bail', bail_id=pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="contrat_bail_{bail.id}.pdf"'

    HTML(string=html_string).write_pdf(response)
    return response
