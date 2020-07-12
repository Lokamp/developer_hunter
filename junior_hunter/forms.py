from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from junior_hunter.models import Company, Vacancy, Specialty, Application, Resume


class RegForm(UserCreationForm):
    username = forms.CharField(
        max_length=50,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        max_length=50,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=50,
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=50,
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    password2 = forms.CharField(
        label='Введите пароль еще раз',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = User
        fields = [
            'username', 'email',
            'first_name', 'last_name',
            'password1', 'password2'
        ]


class CompanyInfoForms(forms.ModelForm):
    logo = forms.ImageField(
        label='Загрузите картинку'
    )

    class Meta:
        model = Company
        fields = [
            'name', 'location',
            'logo', 'description',
            'employee_count'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'employee_count': forms.NumberInput(attrs={'class': 'form-control'})
        }


class VacancyForm(forms.ModelForm):
    speciality = forms.ModelChoiceField(
        Specialty.objects.all(),
        label='Специальность',
        empty_label="Выберите специальность",
        widget=forms.Select(
            attrs={'class': 'form-control', 'label': 'label'}
        )
    )

    class Meta:
        model = Vacancy
        exclude = [
            'company'
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'skills': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AppForm(forms.ModelForm):

    class Meta:
        model = Application

        exclude = [
            'vacancy',
            'user'
        ]

        widgets = {
            'written_username': forms.TextInput(attrs={'class': 'form-control'}),
            'written_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'written_cover_letter': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ResumeForm(forms.ModelForm):
    specialty = forms.ModelChoiceField(
        Specialty.objects.all(),
        label='Специальность',
        empty_label="Выберите специальность",
        widget=forms.Select(
            attrs={'class': 'form-control', 'label': 'label'}
        )
    )
    status = forms.ChoiceField(
        choices=Resume.ResumeStatusChoices.choices,
        initial='NW',
        label='Специальность',
        widget=forms.Select(
            attrs={'class': 'form-control', 'label': 'label'}
        )
    )
    grade = forms.ChoiceField(
        choices=Resume.ResumeGradeChoices.choices,
        label='Специальность',
        widget=forms.Select(
            attrs={'class': 'form-control', 'label': 'label'}
        )
    )

    class Meta:
        model = Resume
        exclude = [
            'user'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'education': forms.Textarea(attrs={'class': 'form-control'}),
            'experience': forms.Textarea(attrs={'class': 'form-control'}),
            'portfolio': forms.TextInput(attrs={'class': 'form-control'}),
        }
