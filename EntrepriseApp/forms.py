from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur

class RegisterUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Utilisateur
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'role', 'telephone')