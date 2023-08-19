from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from charge import views

urlpatterns = [
    path('sellers/', views.SellerList.as_view()),
    path('sellers/<int:pk>/', views.SellerDetail.as_view()),
    path('customers/', views.CustomerList.as_view()),
    path('customers/<str:phone>/', views.CustomerDetail.as_view()),
    path('credits/', views.CreditRequestList.as_view()),
    path('charges/', views.ChargeRequestList.as_view()),
    path('charges/<int:pk>/charge', views.ChargeRequestCharge.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
