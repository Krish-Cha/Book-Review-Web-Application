from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-book/', views.add_book, name='add_book'),
    path('add-review/<int:book_id>/', views.add_review, name='add_review'),
]