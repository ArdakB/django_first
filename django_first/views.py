from django.http import HttpResponse
from django.shortcuts import render
from .models import Order


def hello(request):
    return render(request, 'hello.html')


def order(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order.html', context={
        'order': order
    })


def bye(request):
    return HttpResponse('Bye, world!')


def third(request):
    return HttpResponse('Third')
