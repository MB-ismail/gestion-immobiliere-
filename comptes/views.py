from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import CustomUser
from .forms import CustomUserCreationForm


# ----------------------------
# ✅ Inscription
# ----------------------------
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique après inscription
            return redirect('dashboard')  # Redirection vers tableau de bord
    else:
        form = CustomUserCreationForm()
    return render(request, 'comptes/signup.html', {'form': form})


# ----------------------------
# ✅ Connexion
# ----------------------------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirection vers le bon dashboard
    else:
        form = AuthenticationForm()
    return render(request, 'comptes/login.html', {'form': form})


# ----------------------------
# ✅ Déconnexion
# ----------------------------
def logout_view(request):
    logout(request)
    return redirect('login')


# ----------------------------
# ✅ Tableau de bord selon le rôle
# ----------------------------
@login_required
def dashboard_view(request):
    user = request.user
    if user.role == 'proprietaire':
        from biens.models import DemandeBail
        demandes = DemandeBail.objects.filter(bien__proprietaire=user, statut='en attente')
        return render(request, 'comptes/dashboard_proprietaire.html', {'demandes': demandes})
    elif user.role == 'locataire':
        return render(request, 'comptes/dashboard_locataire.html')
    else:
        return render(request, 'comptes/dashboard_agent.html')

