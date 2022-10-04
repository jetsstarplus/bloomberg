import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from filesManager.models import FileSetup, NumberSeries

# from django.contrib.auth.models import User
from mpesa.daraja import lipa_na_mpesa
from users.plan_manager import get_create_order, get_create_plan
from .models import Initiate, C2BPaymentModel, Paypal, Transaction, PaymentModeChoices, TransactionTypeChoices
from users.models import Order, Product

@login_required
def lipa_mpesa(request, prod):
    """This method confirms the the mpesa online transaction and stores initiates the online mpesa"""
    template_name="lipa.html"
    error=None
    message='Enter the correct phone number'
    state=False
    user=request.user
    site = get_current_site(request)
    product= Product.objects.get(pk=prod)
    order = get_create_order(product, user,2)
    """The data is submitted with ajax"""
    if request.is_ajax() and user:
        phone_number = str(request.POST.get("phone", None))
        amount = product.price
        # messages.add_message(request, messages.INFO, f"Hello {username}")
        phone_number=phone_number.strip()
        phone = len(phone_number)
        options = {
            10: phone_number[1:phone],
            12: phone_number[3:phone],
            13: phone_number[4:phone],
            9: phone_number,
        }
        if phone in options.keys:
            phone_number = options[phone]
            state= True

        if state:
            try:
                phone_number=int('254'+phone_number)
            except:
                message="Your Phone number was not correct!"
                messages.add_message(request, messages.WARNING,  error)
            try:
                result = lipa_na_mpesa(phone_number, amount, order.order_no, 'Payment')
                r_json = result.json()
                message = " You can now enter the pin in your phone to finish the payment!"
                merchant= r_json['MerchantRequestID']
                code=r_json['ResponseCode']
                description= r_json['ResponseDescription']
                checkout= r_json['CheckoutRequestID']
                error = description;
                if result.status_code ==200:
                    
                    """Storing the started transaction for future confirmation with the checkout and merchant Id"""
                    initiated = Initiate(
                        MerchantRequestID=merchant,
                        CheckoutRequestID=checkout,
                        ResultCode=code,
                        ResultDescription=description,
                        user=user,
                        mode='mpesa-stk-push',
                        reference=order.order_no)
                    initiated.save()
                    # print(initiated.user)
                    # print(r_json)
                    data = {'message':message, 'status':200, }
                else:
                    data = {'message':error, 'status':200, }
            except:
                message="There Was A Connection Error!"
                data = {'message':message,'status':500,}

            return JsonResponse(data)

            # print(jfile)
            # new_data=ast.literal_eval(test)
            # print(new_data)
            # # result = json.loads(jfile)
            # print(result)

            # print(merchant)

    context={
        'error':error,
        'site': site,
        'product': product
    }
    return render(request, template_name=template_name, context=context)

@login_required
def paybill(request, prod):
    """An admin method for taking the mpesa transaction from c2b and confirm with the ones stored
    in the confirmation endpoint
    The method also checks if the transaction has already been confirmed for more security reasons"""
    template_name="paybill.html"
    message=None
    user=request.user
    paybill='601393'
    site = get_current_site(request)
    user= request.user
    product= Product.objects.get(pk=prod)
    order = get_create_order(product, user,2) 
    # print(string)
    # base=base64.b64decode(string.encode('ascii')).decode('ascii')
    # print(base)
    if request.is_ajax() and user:
        trans = str(request.POST.get("trans", None))
        # messages.add_message(request, messages.INFO, f"Hello {username}")
        transaction=C2BPaymentModel.objects.filter(TransID=trans)
        if transaction:
                message = " You Can Now Proceed with uploading your content!"
                data={
                    'message':message,
                    'status':200
                }
        else:
            data={
                'message':'Transaction ID Not Found!',
                'status':404
            }
        return JsonResponse(data)

    context={
        'account':order.order_no,
        'paybill':paybill,
        'site': site,
        'product': product,
        'amount': order.price
    }
    return render(request, template_name=template_name, context=context)

@xframe_options_sameorigin
def paypal(request):
    """A method that is used to get the transaction after a successfull paypall transaction"""

    # print(json.load(request)['name'])
    if request.is_ajax() and request.method=='POST' and request.user:
        # getting the data from the ajax json
        data=json.load(request)['data']

        name=data['name']
        amount=data['amount']
        user=request.user
        id= data['id']
        status=data['status']
        currency=data['currency']
        amount=data['amount']

        if request.user.get_full_name():
            user_name=request.user.get_full_name()
        else:
            user_name=request.user.username

        transaction=Paypal(user=user, name=name, amount=amount, currency=currency, paypal_id=id)
        initiated = Initiate(
                    CheckoutRequestID=id,
                    ResultCode=0,
                    ResultDescription=currency,
                    user=user,
                    mode=1)
        initiated.complete()
        initiated.save()

        # print(transaction)
        if status=='COMPLETED':
            transaction.save()
            data={
                'message':'Payment Successful!',
                'status':200
            }
        else:
            data={
                'message':'Payment Failed!',
                'status':400
            }

        return JsonResponse(data)
class TransactionList(ListView, LoginRequiredMixin):
    template_name = 'transactions.html'
    paginate_by = 8
    
    def get_context_data(self,**kwargs):
        context = super(TransactionList,self).get_context_data(**kwargs)
        context['site'] = get_current_site(self.request)
        return context
    
    def get_queryset(self):
        queryset = Transaction.objects.filter(user= self.request.user)
        return queryset

@login_required
def process_payment(request):
    order_id = request.session.get('order_id')
    # order = get_object_or_404(Order, id=order_id)
    host = request.get_host()
    amount = 10

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % amount,
        'item_name': 'Order {}'.format("test"),
        'invoice': str("order.id"),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payments:payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payments:payment_cancelled')),
    }

    # form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'paypal/process_payment.html', {'form': form})


@csrf_exempt
def payment_done(request):
    return render(request, 'paypal/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'paypal/payment_cancelled.html')

class PayByCheque(View):    
    def get(self, request, prod):        
        user= request.user
        product = Product.objects.get(pk=prod)
        order = get_create_order(product, user,1)               
        get_create_plan(order, user, product, PaymentModeChoices.CHEQUE, order.order_no)
        return redirect('payments:transactions')    
