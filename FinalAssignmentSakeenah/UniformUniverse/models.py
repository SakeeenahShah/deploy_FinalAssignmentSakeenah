from django.db import models

# Create your models here.

class Customer(models.Model):
    CustomerID=models.AutoField(primary_key=True)
    Email=models.EmailField(unique=True)
    CustomerName=models.TextField()
    Password=models.CharField(max_length=50)
    PhoneNo=models.CharField(max_length=12)
    Address=models.TextField()

class Uniform(models.Model):
    UniformID=models.CharField(max_length=3, primary_key=True)
    UniformName=models.TextField()
    Price=models.DecimalField(max_digits=5, decimal_places=2)
    Stock=models.IntegerField()

class Order_Details(models.Model):
    OrderID=models.AutoField(primary_key=True)
    CustomerID=models.ForeignKey(Customer, on_delete=models.CASCADE)
    UniformID=models.ForeignKey(Uniform, on_delete=models.CASCADE)
    Quantity=models.IntegerField()
    Total_Price=models.DecimalField(max_digits=10, decimal_places=2)
    Status=models.CharField(max_length=10, default="Pending")

class Review(models.Model):
    ReviewID=models.CharField(max_length=2, primary_key=True)
    OrderID=models.ForeignKey(Order_Details, on_delete=models.CASCADE)
    Description=models.TextField()
    Date=models.DateField()