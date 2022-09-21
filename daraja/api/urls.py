from django.urls import path
from daraja.api import views as apiviews

app_name='payments'
urlpatterns = [
    path("lmmapi/", apiviews.Lipa_List.as_view(), name ="LipaNaMpesaCallbackApi"),
    path("lmmapi/validate/", apiviews.Customer_to_Business_Validate.as_view(), name ="C2BValidationUrl"),
    path("lmmapi/confirm/", apiviews.Customer_to_Business_Confirm.as_view(), name ="C2BConfirmationUrl"),
    path("lmmapi/balance/", apiviews.Lipa_na_Mpesa_Balance.as_view(), name ="BusinessBalanceUrl"),
    path("lmmapi/qeuetimeout/", apiviews.Lipa_na_Mpesa_QeueTimeOut.as_view(), name ="BusinessQuetimeOut"),
    path('b2c/queue/timeout', apiviews.BTC_queue_timeout.as_view(), name='btc_queue_timeout'),
    path('b2c/result/', apiviews.BTC_result.as_view(), name='btc_results'),
    path('lmmapi/api/status/', apiviews.Transaction_Status.as_view(), name = 'transaction_status'),    
]
