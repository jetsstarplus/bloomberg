from datetime import timedelta
from xmlrpc.client import Boolean
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from daraja.models import  Transaction, TransactionTypeChoices
from filesManager.models import FileSetup, NumberSeries
from users.models import Plan, Order, PlanEntries


def get_create_order(product, user,mode_of_payment):
    file_setup = FileSetup.objects.get(pk=1)
    try:
        no_series = NumberSeries.objects.get(pk=file_setup.order_no_series.pk)
    except(ObjectDoesNotExist):
        raise('Setup transactions Number Series in file Setup')
    try:
        order = Order.objects.get(product=product, user=user, paid=False)
    except(ObjectDoesNotExist):
        order = Order.objects.create(
            order_no=no_series.get_next_no(),
            product=product,
            user=user, 
            price=product.price, 
            storage_size=product.storage_size, 
            mode_of_payment=mode_of_payment,
            period=product.period
            )
    return order

def get_create_plan(order, user, product, payment_mode, ref_no)->Boolean:
    file_setup = FileSetup.objects.get(pk=1)
    try:
        no_series = NumberSeries.objects.get(pk=file_setup.transaction_no_series.pk)
    except(ObjectDoesNotExist):
        raise('Setup transactions Number Series in file Setup')
    transaction_no= no_series.get_next_no()
    transaction = Transaction(
        transaction_id = transaction_no,
        mode = payment_mode,
        amount = order.price,
        trans_type = TransactionTypeChoices.CREDIT, 
        user = user,
        reference=ref_no
        )
    
    transaction.success()
    transaction.save()
    Plan.objects.filter(user=user, expired=True).update(current=False)
    try:
        plan = Plan.objects.get(user=user, product=product)
    except(ObjectDoesNotExist):
        plan= Plan(
            product=product,
            user=user,
            price=order.price, 
            storage_size=order.storage_size,
            period=order.period,
            current=True
            )
    last_expiry_date= timezone.now()
    if plan.date_expired > last_expiry_date:
        last_expiry_date = plan.date_expired
    plan.current=True
    plan.date_expired = calculate_expiry_date(last_expiry_date, order.period)
    plan.save()
    order.paid=True
    order.save()
    create_plan_entries(plan, order, transaction_no)
    return True

def create_plan_entries(plan, order, transaction):
    plan_entry = PlanEntries(
        plan=plan,
        order= order,
        price=plan.price,
        amount=order.price,
        storage_size=order.storage_size,
        period=order.period,
        date_expired = calculate_expiry_date(timezone.now(), order.period),
        paid=True,
        transaction_no= transaction
    )
    plan_entry.save()

def calculate_expiry_date(date, months):
    return(date + timedelta(days=months*30))