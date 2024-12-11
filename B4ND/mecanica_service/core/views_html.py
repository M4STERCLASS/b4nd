from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django import forms
from .models import Service, Booking, MechanicProfile

#form. de registro
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirmar contraseña")

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password2')
        if p1 != p2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cleaned_data

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            return redirect('login_view')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

#form. de login
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                form.add_error('username', 'Credenciales inválidas')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

def home_view(request):
    return render(request, 'home.html')

#form. para crear servicios
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'category', 'details', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

@login_required
def services_view(request):
    #lista todos los servicios
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})

@login_required
def book_service(request, service_id):
    #reserva un servicio
    service = get_object_or_404(Service, id=service_id)
    Booking.objects.create(
        user=request.user,
        service=service,
        date=timezone.now().date(),
        status='PEND'
    )
    return redirect('my_bookings')

@login_required
def my_bookings(request):
    #muestra las reservas del usuario
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})

@login_required
def add_service_view(request):
    #solo mecánicos pueden agregar servicios
    try:
        mechanic_profile = request.user.mechanicprofile
    except MechanicProfile.DoesNotExist:
        return HttpResponse("No eres un mecánico. Primero hazte mecánico para ofrecer servicios.")
    
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.mechanic = mechanic_profile
            service.save()
            return redirect('services_view')
    else:
        form = ServiceForm()

    return render(request, 'add_service.html', {'form': form})

@login_required
def become_mechanic_view(request):
    # Crea un perfil de mecánico para el usuario actual, si no existe
    MechanicProfile.objects.get_or_create(user=request.user)
    return redirect('services_view')
