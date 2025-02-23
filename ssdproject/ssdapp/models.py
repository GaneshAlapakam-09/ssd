from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

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


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice {self.invoice_number}"
    



class ProductMaster(models.Model):
    Product_Id = models.CharField(primary_key=True, max_length=50)
    Product_Name = models.CharField(max_length=50)
    GST = models.CharField(max_length=50)
    HSN_Code = models.CharField(max_length=50)
    Status = models.IntegerField(default=1)


    def __str__(self):
        return self.Product_Name
    
class CategoriesMaster(models.Model):
    Categories_Id = models.CharField(primary_key=True, max_length=50)
    Categories_Name = models.CharField(max_length=50)
    Product_Name = models.CharField(max_length=50)
    Sub_Categories = models.CharField(null=True, max_length=50)
    Status = models.IntegerField(default=1)

    def __str__(self):
        return self.Categories_Name
    

class CostMaster(models.Model):
    Cost_Id = models.CharField(primary_key = True , max_length=50)
    Product_Name = models.CharField( max_length=50)
    Category_Name = models.CharField( max_length=50)
    Sub_Category = models.CharField(null=True, max_length=50)
    Cost_Per_Unit_Status = models.IntegerField(default=0)
    Cost_Per_Unit = models.IntegerField(default=0)
    Cost_Per_Sqft_Status = models.IntegerField(default=0)
    Cost_Per_Sqft = models.IntegerField(default=0)
    Status = models.IntegerField(default=1)

    def __str__(self):
        return self.Product_Name
    

class BillingMaster(models.Model):
    Bill_Id = models.CharField(primary_key = True , max_length=50)
    Customer_Id = models.CharField(max_length=50)
    Customer_Name =models.CharField(max_length=50)
    Phone_No = models.BigIntegerField()
    Grand_Total = models.IntegerField()
    Grand_Total_With_Gst = models.IntegerField()
    Status = models.IntegerField(default=1)


    def __str__(self):
        return self.Bill_Id

class BillingDetails(models.Model):
    Bill_Id = models.ForeignKey("ssdapp.BillingMaster", on_delete=models.CASCADE)
    Customer_Id = models.CharField(max_length=50)
    Customer_Name =models.CharField(max_length=50)
    Phone_No = models.BigIntegerField()
    Product_Name = models.CharField(max_length=50)
    Custom_Product = models.CharField(max_length=50)
    Category_Name = models.CharField( max_length=50)
    Sub_Category = models.CharField(null=True, max_length=50)
    Length = models.IntegerField(default=0)
    Width = models.IntegerField(default=0)
    Quantity = models.IntegerField(default=0)
    Cost_Per_Quantity = models.IntegerField(default=0)
    GST = models.CharField(max_length=50)
    HSN_Code = models.CharField(max_length=50)
    Total_Cost = models.CharField(max_length=50)
    Total_Cost_With_Gst = models.CharField(max_length=50)
    Status = models.IntegerField(default=1)

    def __str__(self):
        return self.Bill_Id
    


class QuoteMaster(models.Model):
    Quote_Id = models.CharField(primary_key = True , max_length=50)
    Customer_Id = models.CharField(max_length=50)
    Customer_Name =models.CharField(max_length=50)
    Phone_No = models.BigIntegerField()
    Grand_Total = models.IntegerField()
    Grand_Total_With_Gst = models.IntegerField()
    Status = models.IntegerField(default=1)


    def __str__(self):
        return self.Quote_Id
    

class QuoteDetails(models.Model):
    Quote_Id = models.ForeignKey("ssdapp.QuoteMaster", on_delete=models.CASCADE)
    Customer_Id = models.CharField(max_length=50)
    Customer_Name =models.CharField(max_length=50)
    Phone_No = models.BigIntegerField()
    Product_Name = models.CharField(max_length=50)
    Custom_Product = models.CharField(max_length=50)
    Category_Name = models.CharField( max_length=50)
    Sub_Category = models.CharField(null=True, max_length=50)
    Length = models.IntegerField(default=0)
    Width = models.IntegerField(default=0)
    Quantity = models.IntegerField(default=0)
    Cost_Per_Quantity = models.IntegerField(default=0)
    GST = models.CharField(max_length=50)
    HSN_Code = models.CharField(max_length=50)
    Total_Cost = models.CharField(max_length=50)
    Total_Cost_With_Gst = models.CharField(max_length=50)
    Status = models.IntegerField(default=1)


    def __str__(self):
        return self.Quote_Id
    


class EstimateMaster(models.Model):
    Estimation_Id = models.CharField(primary_key = True , max_length=50)
    Customer_Id = models.CharField(max_length=50)
    Customer_Name =models.CharField(max_length=50)
    Phone_No = models.BigIntegerField()
    Grand_Total = models.IntegerField()
    Status = models.IntegerField(default=1)


    def __str__(self):
        return self.Estimation_Id
    

class EstimateDetails(models.Model):
    Estimation_Id = models.ForeignKey("ssdapp.EstimateMaster", on_delete=models.CASCADE)
    Customer_Id = models.CharField(max_length=50)
    Customer_Name =models.CharField(max_length=50)
    Phone_No = models.BigIntegerField()
    Product_Name = models.CharField(max_length=50)
    Custom_Product = models.CharField(max_length=50)
    Category_Name = models.CharField( max_length=50)
    Sub_Category = models.CharField(null=True, max_length=50)
    Length = models.IntegerField(default=0)
    Width = models.IntegerField(default=0)
    Quantity = models.IntegerField(default=0)
    Cost_Per_Quantity = models.IntegerField(default=0)
    Total_Cost = models.CharField(max_length=50)
    Status = models.IntegerField(default=1)


    def __str__(self):
        return self.Estimation_Id
    


class Employee(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    emp_id = models.CharField(max_length=20, unique=True)
    phone = models.IntegerField(unique=True)
    DOJ = models.DateField(null=True)
    blood_group = models.CharField(max_length=5)
    aadhar = models.CharField(max_length=20, unique=True)
    pan = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=50 , null=True)

    # Add related_name to avoid conflicts with auth.User
    groups = models.ManyToManyField(Group, related_name="employee_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="employee_permissions", blank=True)