from django.db import models

from django.contrib.auth.models import User

from .exceptions import PaymentException, StoreException


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
        related_name='store_items'
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
        try:
            store = Store.objects.get(
                location=Location.objects.get(city=self.city)
            )
        except (Store.DoesNotExist, Location.DoesNotExist):
            raise StoreException('Location not available')
        for item in self.order_items.all():
            store_item = StoreItem.objects.get(
                store=store,
                product=item.product
            )
            if item.quantity > store_item.quantity:
                raise StoreException('Not enough stock')
            store_item.quantity -= item.quantity
            store_item.save()
        self.price = sum(
            (item.product.price * item.quantity
                for item in self.order_items.all())
        )
        confirmed_payments = self.payments.filter(is_confirmed=True)
        paid_amount = sum((payment.amount for payment in confirmed_payments))
        if paid_amount < self.price:
            raise PaymentException('Not enough money')
        self.is_paid = True
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
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
