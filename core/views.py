from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.db.models import Q

# Create your views here.
def index_view(request, *args, **kwargs):
    return render(request, 'core/index.html', {})