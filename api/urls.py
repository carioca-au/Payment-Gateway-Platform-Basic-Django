from django.urls import path

from api import views

urlpatterns = [
    path('payments/<int:company_id>', views.payment_list),
    path('payments/<int:company_id>/<int:payment_id>', views.payment_detail),

    path('subscription/<int:company_id>', views.subscription),


    path('email/<int:company_id>', views.email),
    path('email_list', views.email_list),

]
