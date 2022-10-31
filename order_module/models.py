from django.db import models
from Acount_module.models import UserAcount
from bookModel_module.models import BookModels


class Order(models.Model):
    user = models.ForeignKey(UserAcount, on_delete=models.CASCADE, verbose_name='User')
    is_paid = models.BooleanField(verbose_name='Is Paid')
    payment_date = models.DateField(null=True, blank=True, verbose_name='Payment date')

    def __str__(self):
        return str(self.user)

    def calculate_total_price(self):
        total_amount = 0
        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.final_price * order_detail.count
        else:
            for order_detail in self.orderdetail_set.all():
                if order_detail.product.offer:
                    total_amount += order_detail.product.offer_price * order_detail.count
                else:
                    total_amount += order_detail.product.price * order_detail.count
        return float(total_amount)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Cart')
    product = models.ForeignKey(BookModels, on_delete=models.CASCADE, verbose_name='Product')
    final_price = models.FloatField(null=True, blank=True, verbose_name='Final Pirce')
    count = models.IntegerField(verbose_name='Count')

    def get_total_price(self):
        if self.product.offer:
            return self.count * self.product.offer_price
        else:
            return self.count * self.product.price

    def __str__(self):
        return str(self.order)
