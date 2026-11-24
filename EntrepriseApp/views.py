from django.shortcuts import render
from django.shortcuts import redirect
from .forms import RegisterUserForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = RegisterUserForm()
    return render(request, 'register.html', {'form': form})