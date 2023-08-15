"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from src.book.views import api_book_list, api_book_borrower, api_book_detail
from src.borrow.views import api_borrow_book, api_renew_book, api_return_book
from src.iam.views import api_user_registration, api_user_login, api_user_profile

router = routers.DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),

    # IAM
    path('register', api_user_registration, name='api-user-registration'),
    path('login', api_user_login, name='api-user-login'),
    path('me', api_user_profile, name='api-user-profile'),

    # Book
    path('books', api_book_list, name='api-book-list'),
    path('book/<book_id>', api_book_detail, name='api-book-detail'),
    path('book/<book_id>/borrower', api_book_borrower, name='api-book-borrower'),

    # Borrow
    path('borrow', api_borrow_book, name='api-borrow-book'),
    path('renew', api_renew_book, name='api-renew-book'),
    path('return', api_return_book, name='api-return-book'),
]
