from django.db import models
from products.models import ProductTable
# Create your models here.
from django.contrib.auth.models import User

class User_info(models.Model):
    uid = models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    phone = models.CharField(max_length=10,null=True)
    pincode = models.CharField(max_length=10,null=True)
    address = models.CharField(max_length=200,null=True)
    image = models.FileField(upload_to='images', default='images/default.png')

class Cart_table(models.Model):
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE,db_column="user_id")
    product_id = models.ForeignKey(ProductTable, on_delete=models.CASCADE,db_column="product_id")
    quantity = models.PositiveIntegerField()


class Payment_history(models.Model):
    id=models.CharField(primary_key=True,max_length=20)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,db_column="user_id")
    datetime = models.DateTimeField(auto_now=True)
    amount = models.PositiveIntegerField(null=True)

class Order_history(models.Model):
    payment_id = models.ForeignKey(Payment_history,on_delete=models.CASCADE,db_column="payment_id")
    uid = models.ForeignKey(User,on_delete=models.CASCADE,db_column="user_id")
    product_id = models.ForeignKey(ProductTable,on_delete=models.CASCADE,db_column="product_id")
    price=models.PositiveIntegerField(null=True)
    quantity= models.PositiveIntegerField(null=True)
    date  = models.DateField(auto_now=True)
    address = models.TextField(max_length=100,null=True)