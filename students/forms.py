from django import forms
from .models import Student
from django.contrib.auth.models import User

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'age', 'group', 'photo']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'age': 'Возраст',
            'group': 'Группа (например, ИС-21)',
            'photo': 'Фотография студента'
        }

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label="Логин")
    email = forms.EmailField(required=False, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Подтвердите пароль")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают!")
        return cleaned_data