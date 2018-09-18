from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from djmoney.models.fields import MoneyField


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField()
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    categories = models.ManyToManyField('product.Category')

    @classmethod
    def get_or_none(cls, **kwargs):
        try:
            product = cls.objects.get(**kwargs)
        except cls.DoesNotExist:
            product = None

        return product

    def __str__(self):
        return f"{self.title} -- {self.price}"


class Category(models.Model):
    title = models.CharField(max_length=255)

    class Meta(object):
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.title}"


class DeliveryService(models.Model):
    title = models.CharField(max_length=255)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    class Meta(object):
        verbose_name = "delivery service"
        verbose_name_plural = "delivery services"

    @classmethod
    def get_or_none(cls, **kwargs):
        try:
            delivery_service = cls.objects.get(**kwargs)
        except cls.DoesNotExist:
            delivery_service = None

        return delivery_service

    def __str__(self):
        return f"{self.title} -- {self.price}"


class Order(models.Model):
    user = models.ForeignKey('account.User', related_name='orders', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', related_name='orders', on_delete=models.CASCADE)
    delivery = models.ForeignKey('product.DeliveryService', related_name='orders', on_delete=models.CASCADE)
    products_count = models.PositiveIntegerField()
    invoice = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)


class WishList(models.Model):
    user = models.ForeignKey('account.User', related_name='wishlist', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', related_name='wishlists', on_delete=models.CASCADE)


@receiver(pre_save, sender='product.Order')
def populate_invoiced_amount(sender, instance=None, created=False, **kwargs):
    """
    This is triggered whenever a new Order is just going to be saved
    to the database.

    Arguments:
        sender: sender of this signal
        instance: model instance
        created: boolean indicating if db record was created

    Keyword Arguments:
        kwargs: dict containing keyword arguments
    """
    # the following is just going to be saved into the database.
    instance.invoice = instance.product.price * instance.products_count + instance.delivery.price
