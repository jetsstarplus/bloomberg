from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from daraja.models import PaymentModeChoices
from .forms import UserRegisterForm
from .models import Plan, Product, Order
from filesManager.models import Files
from django.http import JsonResponse
import json
from rest_framework import generics, viewsets, permissions
from users.serializers import UserSerializer
from users.plan_manager import get_create_order, get_create_plan


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    user_files = Files.objects.filter(user=user)
    totalFileSize = (sum([file.file_size for file in user_files]))
    file_count = user_files.count()
    current_plan = False
    try:  
        current_plan = Plan.objects.get(user=user, current=True)
    except:
        pass
    context = {'videos':user_files,'plan':current_plan, 'file_count': file_count,'total_file_size': totalFileSize}
    return render(request, 'users/profile.html', context)

def home(request):
    return render(request, 'users/home.html')


def payment(request):
    product = Product.objects.all
    context = {'product':product}
    return render(request, 'users/payment.html', context)


def checkout(request,pk):
    product = Product.objects.get(id=pk)
    context = {'product':product}
    return render(request, 'users/checkout.html', context)

def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    user=request.user
    product = Product.objects.get(id=body['productId'])
    order = get_create_order(product, user,0)
    get_create_plan(order, user, product, PaymentModeChoices.PAYPAL)
    return JsonResponse('Payment completed!', safe=False)
 

from django.contrib.auth.models import User


class UserList(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
