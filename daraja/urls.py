from django.urls import path, include
from rest_framework import routers
from daraja import views

 #routers provide an easy way of automatically determining the url configurations

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)

app_name = "payments"

urlpatterns = [
    # path("users/", include(router.urls)),
     path('', include('daraja.api.urls')),
     path('lipa/stkpush/<int:prod>/', views.lipa_mpesa, name="lipa_na_mpesa"),
     path('lipa/paybill/confirm/<int:prod>/', views.paybill, name="paybill"),
     path('payment/paypal/',views.paypal, name="paypal" ),
     path('cheque/<int:prod>/',views.PayByCheque.as_view(), name="cheque" ),
     path('transactions/', views.TransactionList.as_view(), name="transactions"),
     path('process-payment/', views.process_payment, name='process_payment'),
     path('payment-done/', views.payment_done, name='payment_done'),
     path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),

]
