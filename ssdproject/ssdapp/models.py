from django.db import models

# Create your models here.

class CustomerMaster(models.Model):
    Customer_Id = models.CharField(primary_key=True, max_length=50)
    Customer_Name =models.CharField(max_length=50)
    Phone_No = models.IntegerField()
    Status = models.IntegerField(default=1)

class CustomerDetails(models.Model):
    Customer_Id = models.CharField(primary_key=True, max_length=50)
    Customer_Name =models.CharField(max_length=50)
    Phone_No = models.BigIntegerField()
    Alt_Phone = models.BigIntegerField()
    Email = models.EmailField(max_length=254)
    Address = models.CharField(max_length=150)
    Status = models.IntegerField(default=1)


class MaterialMaster(models.Model):
    Material_Id = models.CharField(primary_key=True, max_length=50)
    Material_Name = models.CharField( max_length=50)
    Material_Make = models.CharField(max_length=50)
    Material_Size_In_Meters = models.IntegerField()
    Material_Size_In_Feet = models.IntegerField()
    Additional_Info = models.CharField(max_length=50)
    Status = models.IntegerField(default=1)


class InwardMaster(models.Model):
    S_No = models.IntegerField(unique=True)
    Inward_Id = models.CharField(primary_key=True,max_length=50)
    Material_Id = models.CharField( max_length=50)
    Vendor_Name = models.CharField(max_length=50)
    Vendor_Mobile = models.IntegerField()
    Vendor_GST = models.CharField(max_length=50)
    Invoice_Cost = models.IntegerField()
    Invoice_Quantity = models.IntegerField()
    Batch_No = models.CharField(max_length=50)
    Batch_Id = models.CharField(max_length=50)
    Additional_Info = models.CharField(max_length=50)
    Status = models.IntegerField(default=1)



class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
