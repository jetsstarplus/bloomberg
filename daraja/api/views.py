from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from datetime import datetime
import pytz
from django.views import View
from django.http import HttpResponse, HttpResponseForbidden
from django.core.mail import send_mail
from django.conf import settings

#for handling responses
from rest_framework.response import Response


from daraja.api.serializers import Lipa_na_mpesaSerializer, C2BPaymentSerializer
from daraja import models
from users.models import Order
from users.plan_manager import get_create_plan

# from account.models import UserPayment


class Lipa_List(CreateAPIView):
    """This method waits for the response from mpesa and stores the successful transaction information"""
    queryset = models.Lipa_na_mpesa.objects.all()
    serializer_class = Lipa_na_mpesaSerializer
    permission_classes = [AllowAny]


    def create(self, request, *args, **kwargs):
        print(request.data, " Stk push request result")

        merchant_request_id = request.data["Body"]['stkCallback']['MerchantRequestID']
        checkout_request_id = request.data["Body"]['stkCallback']['CheckoutRequestID']
        result_code = request.data["Body"]["stkCallback"]['ResultCode']
        result_description = request.data["Body"]["stkCallback"]["ResultDesc"]
        amount = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
        mpesa_receipt_no = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
        balance = ""
        transaction_date = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"]
        phone_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]

        str_transation_date = str(transaction_date) #changing int datetime to string
        transation_date_time = datetime.strptime(str_transation_date, "%Y%m%d%H%M%S")#changing a string to datetime

        #making transaction datetime to be aware of the timezone
        aware_transaction_datetime = pytz.utc.localize(transation_date_time)

        #creating an instance of our model
        initiated=models.Initiate.objects.get(CheckoutRequestID=checkout_request_id)
        models.Lipa_na_mpesa.objects.create(
            CheckoutRequestID = checkout_request_id,
            MerchantRequestID = merchant_request_id,
            ResultCode = result_code,
            ResultDesc = result_description,
            Amount = amount,
            MpesaReceiptNumber = mpesa_receipt_no,
            Balance = balance,
            TransationDate = aware_transaction_datetime,
            phonenumber = phone_number,

        )
        user=get_user_model().objects.get(pk=initiated.user.pk)
        if result_code==0:
            # Checking if the transaction was successful with result code 0 and changing the user's information to payed
            initiated.ResultDescription=result_description
            initiated.save(update_fields=['ResultDescription'])
            order= Order.objects.get(order_no= initiated.reference)
            get_create_plan(order, user, order.product, mpesa_receipt_no, models.PaymentModeChoices.MPESA, mpesa_receipt_no)           
        else:
            initiated.ResultCode=1
            initiated.save(update_fields=['ResultCode'])
        
        return Response({'ResultDescription': result_description})


class Customer_to_Business_Validate(CreateAPIView):
    def create(self, request):
        print(request.data, " This is the request")
        BillRefNumber=request.data["BillRefNumber"]
        Amount =Decimal(request.data["TransAmount"])

        order=Order.objects.get(order_no=BillRefNumber, paid=False)
        if Amount != order.price:
            return HttpResponseForbidden(content = "Amount Specified Does match order {}".format(BillRefNumber), content_type="application/json")
        return HttpResponse(content="Success", status=200, reason="Order No {} for Amount {} Matched".format(BillRefNumber, order.price), content_type='application/json', charset="utf-8")

class Customer_to_Business_Confirm(CreateAPIView):
    """This method stores the information from the customer to business transaction"""
    queryset = models.C2BPaymentModel.objects.all()
    serializer_class = C2BPaymentSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        print(request.data, " This is the request")

        TransactionType=request.data["TransactionType"]
        TransID=request.data["TransID"]
        TransTime=request.data["TransTime"]
        TransAmount=request.data["TransAmount"]
        BusinessShortCode=request.data["BusinessShortCode"]
        BillRefNumber=request.data["BillRefNumber"]
        InvoiceNumber=request.data["InvoiceNumber"]
        OrgAccountBalance=request.data["OrgAccountBalance"]
        ThirdPartyTransID=request.data["ThirdPartyTransID"]
        MSISDN=request.data["MSISDN"]
        FirstName=request.data["FirstName"]
        MiddleName=request.data["MiddleName"]
        LastName=request.data["LastName"]

        str_transation_date = str(TransTime) #changing int datetime to string
        transation_date_time = datetime.strptime(str_transation_date, "%Y%m%d%H%M%S")#changing a string to datetime

        #making transaction datetime to be aware of the timezone
        aware_transaction_datetime = pytz.utc.localize(transation_date_time)

        mpesa_model=models.C2BPaymentModel(
            TransactionType=TransactionType,
            TransID=TransID,
            TransTime=aware_transaction_datetime,
            TransAmount=TransAmount,
            BusinessShortCode=BusinessShortCode,
            BillRefNumber=BillRefNumber,
            InvoiceNumber=InvoiceNumber,
            OrgAccountBalance=OrgAccountBalance,
            ThirdPartyTransID=ThirdPartyTransID,
            MSISDN=MSISDN,
            FirstName=FirstName,
            MiddleName=MiddleName,
            LastName=LastName
        )

        # Marking the mpesa model as complete
        mpesa_model.complete()
        # the actual transaction is saved at the transaction confirmation stage
        mpesa_model.save()
        order = Order.objects.get(order_no=BillRefNumber)
        get_create_plan(order, order.user, order.product, models.PaymentModeChoices.MPESA,TransID)
        return HttpResponse("success")


#this method is used to get the balance
class Lipa_na_Mpesa_Balance(CreateAPIView):
    queryset = None
    serializer_class = None
    permission_classes = [AllowAny]

    def create(self, request):
        print(request.data, " This is the balance request")
        return Response({'ResultDesc': 0})


#a general method for handling the qeuetime out of all the requests
class Lipa_na_Mpesa_QeueTimeOut(CreateAPIView):
    queryset = None
    serializer_class = None
    permission_classes = [AllowAny]

    def create(self, request):
        print(request.data, " This is the qeue time out request")
        return Response({'ResultDesc': 0})



#a general method for handling the qeuetime out of all the requests
class BTC_queue_timeout(CreateAPIView):
    queryset = None
    serializer_class = None
    permission_classes = [AllowAny]

    def create(self, request):
        print(request.data, " This is the qeue time out request for business to customer payment")
        return Response({'ResultDesc': 0})

class BTC_result(CreateAPIView):
    queryset = None
    serializer_class = None
    permission_classes = [AllowAny]

    def create(self, request):
        print(request.data, " This is the success data for business to customer payment")
        return Response({'ResultDesc': 0})

class Transaction_Status(CreateAPIView):
    queryset = None
    serializer_class = None
    permission_classes = [AllowAny]

    def create(self, request):
        print(request.data, " This is the qeue time out request for business to customer payment")
        return Response({'ResultDesc': 0})
