from django.shortcuts import render
from .serializers import UserSerializer, GroupSerializer
from rest_framework import viewsets
from rest_framework import permissions
from .models import User
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomPasswordChangeForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

# Create your views here.
# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('stock:home') # utilisez le nom complet de l'URL
    template_name = 'register.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('landingpage:landing')
            return redirect('stock:home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('landingpage:landing')


def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('home')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})
