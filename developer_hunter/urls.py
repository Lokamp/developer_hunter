from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from junior_hunter.views import (
    MainView, VacanciesView, VacancyView,
    VacancyInCategoryView, CompanyView,
    custom_handler404, custom_handler500,
    RegistrationView, AuthView,
    RegistrationsConfirm, logout_view,
    CompanyProfileVacancyList, CreateCompanyProfile,
    CompanyProfileInfo, CompanyProfileInfoEdit,
    UserProfile, CreateCompanyProfileVacancy,
    CompanyProfileVacancy, CompanyProfileVacancyEdit,
    sent, ResumeView, CreateResume, SearchView,
    about, all_company
)

urlpatterns = [
    path(
        'admin/', admin.site.urls
    ),
    path(
        '',
        MainView.as_view(),
        name='index'
    ),
    path(
        'about/',
        about,
        name='about'
    ),
    path(
        'all_company/',
        all_company,
        name='all_company'
    ),
    path(
        'search/',
        SearchView.as_view(),
        name='search'
    ),
    path(
        'logout/',
        logout_view,
        name='logout'
    ),
    path(
        'login/',
        AuthView.as_view(),
        name='login'
    ),
    path(
        'sent/',
        sent,
        name='sent'
    ),
    path(
        'registration_company/',
        RegistrationView.as_view(),
        name='reg_company'
    ),
    path(
        'registrations_confirm/',
        RegistrationsConfirm.as_view(),
        name='reg_confirm'
    ),
    path(
        'user_profile/',
        UserProfile.as_view(),
        name='user_profile'
    ),
    path(
        'profile/company_create/',
        CreateCompanyProfile.as_view(),
        name='company_create'
    ),
    path(
        'profile/company_info/',
        CompanyProfileInfo.as_view(),
        name='company_profile_info'
    ),
    path(
        'profile/company_info_edit/<int:company_id>/',
        CompanyProfileInfoEdit.as_view(),
        name='company_info_edit'
    ),
    path(
        'profile/company_vacancy_create/',
        CreateCompanyProfileVacancy.as_view(),
        name='company_vacancy_create'
    ),
    path(
        'profile/company_vacancy_list/',
        CompanyProfileVacancyList.as_view(),
        name='company_profile_vacancy'
    ),
    path(
        'profile/company_vacancy/<int:vacancy_id>/',
        CompanyProfileVacancy.as_view(),
        name='company_vacancy'
    ),
    path(
        'profile/company_vacancy_edit/<int:company_id>/',
        CompanyProfileVacancyEdit.as_view(),
        name='company_vacancy_edit'
    ),
    path(
        'profile/resume/',
        ResumeView.as_view(),
        name='resume'
    ),
    path(
        'profile/resume_create/',
        CreateResume.as_view(),
        name='resume_create'
    ),
    path(
        'vacancies/',
        VacanciesView.as_view(),
        name='vacancies'
    ),
    path(
        'vacancies/<int:vacancy_id>/',
        VacancyView.as_view(),
        name='vacancy_id'
    ),
    path(
        'companies/<int:company_id>/',
        CompanyView.as_view(),
        name='company_id'
    ),
    path(
        'vacancies/cat/<str:vacancy_in_category>/',
        VacancyInCategoryView.as_view(),
        name='vacancy_in_category'
    )
]

handler404 = custom_handler404
handler500 = custom_handler500


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
