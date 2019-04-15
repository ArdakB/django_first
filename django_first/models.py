from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )


class Store(models.Model):
    location = models.CharField(max_length=100)


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
    location = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    is_paid = models.BooleanField(default=False)

    def process(self):
        store = Store.objects.get(location=self.location)
        for item in self.order_items.all():
            store_item = StoreItem.objects.get(
                store=store,
                product=item.product
            )
            if item.quantity > store_item.quantity:
                raise Exception('Not enough stock')
            store_item.quantity -= item.quantity
            store_item.save()
        self.price = sum(
            (item.product.price * item.quantity
                for item in self.order_items.all())
        )
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


class Customer(models.Model):
    name = models.CharField(max_length=100)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='customers'
    )
