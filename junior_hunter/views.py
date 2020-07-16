from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from django.db.models import Q

from junior_hunter.forms import RegForm, CompanyInfoForms, VacancyForm, AppForm, ResumeForm
from junior_hunter.models import Specialty, Company, Vacancy, Application, Resume


class MainView(View):
    """Главная страница. Выводятся специальности (до 8) и компании до (16)"""
    def get(self, request):
        number_specialties_main_page = 8
        number_companies_main_page = 16
        specialties = Specialty.objects.all()[:number_specialties_main_page]
        companies = Company.objects.all()[:number_companies_main_page]
        context = {
            'specialties': specialties,
            'companies': companies
        }
        return render(request, 'index.html', context=context)


class SearchView(View):
    """Страница поиска, поиск осуществляется по заголовку и описанию
    ВАЖНО! в sqlite не работает icontains, поэтому поиск чувствителен к регистру"""

    def get(self, request):
        search = request.GET.get('search', '')
        if search:
            vacancies = Vacancy.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))
            context = {
                'vacancies': vacancies,
                'search': search
            }
            return render(request, 'search.html', context=context)
        else:
            messages.info(request, 'Введите запрос')
            return redirect(request.META['HTTP_REFERER'])


class VacanciesView(View):
    """На странице выводятся все вакансии. Необходимо доработать пагинацию!"""

    def get(self, request):
        vacancies = Vacancy.objects.all()
        context = {
            'vacancies': vacancies,
        }
        return render(request, 'vacancies.html', context=context)


class VacancyView(View):
    """Просмотр отдельно взятой вакансии. С возможностью отправить отклик.
    Отклик может отправлять только зарегистрированный пользователь"""

    def get(self, request, vacancy_id):
        vacancy = Vacancy.objects.get(id=vacancy_id)
        if not vacancy:
            return HttpResponseNotFound(
                f'Нет вакансии с id {vacancy_id}.'
                f' Перейти на <a href="/">Главную страницу</a>')
        form = AppForm
        context = {
            'vacancy': vacancy,
            'form': form
        }
        return render(request, 'vacancy.html', context=context)

    def post(self, request, vacancy_id):
        vacancy = Vacancy.objects.get(id=vacancy_id)
        form = AppForm(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated:
                messages.info(request, 'Необходимо зарегистрироваться')
                return redirect(request.META['HTTP_REFERER'])
            post = form.save(commit=False)
            post.user = request.user
            post.vacancy = vacancy
            post.save()
            return redirect('sent')
        else:
            messages.info(request, 'Форма невалидна')
            return redirect(request.META['HTTP_REFERER'])


def sent(request):
    return render(request, 'sent.html')  # Если отклик успешно отправлен, то выводится страница sent


class CompanyView(View):
    """Просмотр отдельно взятой компании. Внешняя страница."""

    def get(self, request, company_id):
        company = Company.objects.filter(id=company_id).first()
        if not company:
            return HttpResponseNotFound(
                f'Нет компании с id {company_id}.'
                f' Перейти на <a href="/">Главную страницу</a>'
            )
        company_vacancies = Vacancy.objects.filter(company_id=company)
        context = {
            'company': company,
            'company_vacancies': company_vacancies
        }
        return render(request, 'company.html', context=context)


class VacancyInCategoryView(View):
    """Страница с вакансиями по конкретной специальности - Backend, Design и т.д."""

    def get(self, request, vacancy_in_category):
        specialty = Specialty.objects.filter(code=vacancy_in_category).first()
        if not specialty:
            return HttpResponseNotFound(
                f'Нет категории {vacancy_in_category}.'
                f' Перейти на <a href="/">Главную страницу</a>')
        vacancies = Vacancy.objects.filter(speciality_id=specialty)
        context = {
            'specialty': specialty,
            'vacancies': vacancies,
        }
        return render(request, 'vacancy_categories.html', context=context)


class UserProfile(View):
    """Страница профиля авторизованного пользователя.
    Скоро добавим возмодность изменения пароля!"""

    def get(self, request):
        user = request.user
        context = {
            'user': user
        }
        return render(request, 'user_profile.html', context=context)


class CreateCompanyProfile(View):
    """Создание компании в профиле, в форму передается пользователь,
    который создает компанию."""

    def get(self, request):
        form = CompanyInfoForms
        context = {
            'form': form
        }
        return render(request, 'company_create.html', context=context)

    def post(self, request):
        user = request.user
        form = CompanyInfoForms(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = user
            form.save()
            return redirect('company_profile_info')
        else:
            messages.info(request, 'Форма невалидна')
            return redirect(request.META['HTTP_REFERER'])


class CompanyProfileInfo(View):
    """Информация о компании в профиле.
    Если компания не создана - идет передресация на страницу создания компании"""

    def get(self, request):
        user = request.user
        if Company.objects.filter(owner=user):
            company = Company.objects.filter(owner=user)
            context = {
                'company': company
            }
            return render(request, 'company_info.html', context=context)
        else:
            return render(request, 'company_not_created.html')


class CompanyProfileInfoEdit(View):
    """Редактирование информации о компании."""

    def get(self, request, company_id):
        company = Company.objects.get(id=company_id)
        if not company:
            return HttpResponseNotFound(
                f'Нет компании с ID {company_id}'
                f' Перейти на <a href="/">Главную страницу</a>'
            )
        form = CompanyInfoForms(instance=company)
        context = {
            'form': form
        }
        return render(request, 'company_edit.html', context=context)

    def post(self, request, company_id):
        company = Company.objects.get(id=company_id)
        company_form = CompanyInfoForms(
            request.POST,
            request.FILES,
            instance=company
        )
        if company_form.is_valid():
            company_form.save()
            messages.success(request, 'Форма обновлена')
            return redirect('company_profile_info')
        else:
            return HttpResponse('Форма невалидна')


class CreateCompanyProfileVacancy(View):
    """Создание вакансии в профиле компании, в форму передается компания,
    которая создает вакансию."""

    def get(self, request):
        form = VacancyForm
        context = {
            'form': form
        }
        return render(request, 'company_vacancy_create.html', context=context)

    def post(self, request):
        user = request.user
        company = Company.objects.get(owner=user)
        form = VacancyForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.company = company
            post.save()
            return redirect('company_profile_vacancy')
        else:
            return HttpResponse('Форма невалидна')


class CompanyProfileVacancyList(View):
    """Список вакансии в профиле компании.
    Если вакансия не создана - идет переадресация на страницу создания вакансии"""

    def get(self, request):
        user = request.user
        company = Company.objects.get(owner=user)

        if Vacancy.objects.filter(company_id=company):
            vacancies = Vacancy.objects.filter(company_id=company)
            context = {
                'vacancies': vacancies
            }
            return render(request, 'company_vacancy_list.html', context=context)
        else:
            return render(request, 'company_vacancy_not_created.html')


class CompanyProfileVacancy(View):
    """Страница вакансии в профиле компании."""

    def get(self, request, vacancy_id):
        vacancy = Vacancy.objects.get(id=vacancy_id)
        apps = Application.objects.filter(vacancy_id=vacancy)
        context = {
            'vacancy': vacancy,
            'apps': apps
        }
        return render(request, 'company_vacancy.html', context=context)


class CompanyProfileVacancyEdit(View):
    """Редактирование информации о компании."""

    def get(self, request, company_id):
        vacancy = Vacancy.objects.get(id=company_id)
        if not vacancy:
            return HttpResponseNotFound(
                f'Нет вакансии с ID {company_id}'
                f' Перейти на <a href="/">Главную страницу</a>'
            )
        form = VacancyForm(instance=vacancy)
        context = {
            'form': form
        }
        return render(request, 'company_vacancy_edit.html', context=context)

    def post(self, request, company_id):
        vacancy = Vacancy.objects.get(id=company_id)
        vacancy_form = VacancyForm(
            request.POST,
            instance=vacancy
        )
        if vacancy_form.is_valid():
            vacancy_form.save()
            messages.success(request, 'Форма обновлена')
            context = {
                'form': vacancy_form
            }
            return render(request, 'company_vacancy_edit.html', context=context)
        else:
            return HttpResponse('Форма невалидна')


class ResumeView(View):
    """Редактирование резюме."""

    def get(self, request):
        user = request.user
        if Resume.objects.filter(user_id=user):
            resume = Resume.objects.filter(user_id=user).first()
            form = ResumeForm(instance=resume)
            context = {
                'form': form
            }
            return render(request, 'resume_edit.html', context=context)
        else:
            return render(request, 'resume_not_create.html')

    def post(self, request):
        user = request.user
        resume = Resume.objects.filter(user_id=user).first()
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.save()
            messages.info(request, 'Форма обновлена')
            return redirect(request.META['HTTP_REFERER'])


class CreateResume(View):
    """Создание резюме, в форму передается пользователь,
    который создает резюме."""

    def get(self, request):
        form = ResumeForm
        context = {
            'form': form
        }
        return render(request, 'resume_create.html', context=context)

    def post(self, request):
        form = ResumeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.info(request, 'Резюме создано!')
            return redirect('resume')
        else:
            return HttpResponse('Форма невалидна')


class RegistrationView(CreateView):
    """Форма регистрации"""
    form_class = RegForm
    success_url = '/registrations_confirm/'
    template_name = 'register_company.html'


class RegistrationsConfirm(LoginView):
    """Страница подтверждения регистрации"""
    redirect_authenticated_user = True
    template_name = 'registrations_confirm.html'


class AuthView(LoginView):
    """Страница аутентификации пользователя"""
    redirect_authenticated_user = True
    template_name = 'registration/login.html'


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


def all_company(request):
    companies = Company.objects.all()
    context = {
        'companies': companies
    }
    return render(request, 'all_company.html', context=context)


def about(request):
    return render(request, 'about.html')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ошибка 404! Попробуйте открыть другую страницу')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка 500! Попробуйте открыть другую страницу')
