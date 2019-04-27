from django.db import models

from django.contrib.auth.models import User

from .exceptions import PaymentException, StoreException, LocationException


class City(models.Model):
    name = models.CharField(max_length=100)


class Location(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='locations'
    )
    address = models.CharField(max_length=100)


class Customer(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )


class Store(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='stores'
    )


class StoreItem(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='store_items'
    )
    quantity = models.IntegerField()


class Order(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    is_paid = models.BooleanField(default=False)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    def process(self):
        city = self.city
        locations = Location.objects.filter(city=city)
        if locations.count() == 0:
            raise LocationException('Location not available')
        stores = Store.objects.filter(location__in=locations)
        if stores.count() == 0:
            raise LocationException('Location not available')
        for item in self.items.all():
            store_items = StoreItem.objects.filter(
                store__in=stores,
                product=item.product
            )
            store_item_quantity = sum(i.quantity for i in store_items)
            if item.quantity > store_item_quantity:
                raise StoreException('Not enough stock')
            difference = item.quantity
            for store_item in store_items:
                if store_item.quantity >= difference:
                    store_item.quantity -= difference
                    store_item.save()
                    difference = 0
                else:
                    store_item.quantity -= store_item.quantity
                    store_item.save()
                    difference -= store_item.quantity
                if difference == 0:
                    break
        confirmed_payments = self.payments.filter(is_confirmed=True)
        paid_amount = sum((payment.amount for payment in confirmed_payments))
        if paid_amount < self.price:
            raise PaymentException('Not enough money')
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    quantity = models.IntegerField()


class Payment(models.Model):
    METHOD_CARD = 'card'
    METHOD_CASH = 'cash'
    METHOD_QIWI = 'qiwi'

    METHOD_CHOICES = (
        (METHOD_CARD, METHOD_CARD),
        (METHOD_CASH, METHOD_CASH),
        (METHOD_QIWI, METHOD_QIWI)
    )

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    method = models.CharField(
        max_length=10,
        choices=METHOD_CHOICES,
        default=METHOD_CARD
    )
    is_confirmed = models.BooleanField(default=False)
