import traceback
from django.shortcuts import render,redirect, get_object_or_404
from ssdapp.models import CustomerMaster,CustomerDetails,MaterialMaster,InwardMaster,Invoice,ProductMaster,CategoriesMaster,CostMaster,BillingMaster,QuoteMaster, EstimateMaster, BillingDetails, QuoteDetails, EstimateDetails, Payment_Master, Payment_Details
from django.contrib import messages

from django.http import HttpResponse
from weasyprint import HTML


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth.hashers import make_password
from .models import Employee
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth import authenticate,login,logout

from datetime import datetime,date,timedelta

import os
from django.core.files.storage import default_storage
# from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

       
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'
def is_employee(user):
    return user.is_authenticated and user.role == 'employee'



def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.info(request,"username and password not match")
            return redirect('signin')
    return render(request,'pages.signin.html')


def dashboard(request):
    return render(request,'dashboard.html')



@login_required(login_url='signin')
def addCustomer(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        altPhone = request.POST['alt_phone']
        email = request.POST['email']
        address = request.POST['address']
        last_customer = CustomerMaster.objects.order_by('-Customer_Id').first()
        if last_customer:
            last_id = int(last_customer.Customer_Id[4:])  # Extract the numeric part
            new_id = f"SSDC{last_id + 1:04d}"
        else:
            new_id = "SSDC0001"

        # phone_list = CustomerDetails.objects.filter(Status = 1).values('Phone_No')

        # phone_no = int(phone) 
        
        # for num in phone_list:
        #     if num["Phone_No"] == phone_no:
        #         messages.info(request,"Phone Number  already exits")
        #         return redirect('addcustomer')

        CustomerMaster.objects.create(Customer_Id = new_id, Customer_Name = name, Phone_No = phone)
        CustomerDetails.objects.create(Customer_Id = new_id, Customer_Name = name, Phone_No = phone, Alt_Phone = altPhone, Email = email, Address = address)

        return redirect('listcustomer')
 
    last_customer = CustomerMaster.objects.order_by('-Customer_Id').first()
    if last_customer:
        last_id = int(last_customer.Customer_Id[4:])  # Extract the numeric part
        new_id = f"SSDC{last_id + 1:04d}"
    else:
        new_id = "SSDC0001"
    
    phone = CustomerDetails.objects.filter(Status = 1)
    context = {'data':new_id, 'phone': phone}

    return render(request,'add_customer.html',context)
@login_required(login_url='signin')
def listCustomer(request):
    data = CustomerDetails.objects.filter(Status = 1)
    context = {'data':data}
    return render(request,'list_customer.html',context)

@login_required(login_url='signin')
def customerDetails(request,id):
    data = CustomerDetails.objects.filter(Customer_Id = id , Status =1)
    context = {'data':data}
    return render(request,'customer_details.html',context)


# def editCustomer_S(request):
#     data = CustomerDetails.objects.filter(Status=1)
#     context = {'data':data}
#     return render(request,'edit_customer_s.html',context)
@login_required(login_url='signin')
def editCustomer(request,id):
    if request.method == 'POST':
        if request.method == 'POST':
            customerId = request.POST['customer_id']
            name = request.POST['name']
            phone = request.POST['phone']
            altPhone = request.POST['alt_phone']
            email = request.POST['email']
            address = request.POST['address']
            CustomerDetails.objects.filter(Customer_Id=customerId).update(Alt_Phone = altPhone, Email = email, Address = address)
            return redirect('listcustomer')

    data = CustomerDetails.objects.filter(Customer_Id = id , Status =1)
    context = {'data':data}
    return render(request,'edit_customer.html',context)
@login_required(login_url='signin')
def deleteCustomer(request,id):
    CustomerDetails.objects.filter(Customer_Id = id).update(Status = 0)
    CustomerMaster.objects.filter(Customer_Id = id).update(Status = 0)
    return redirect('listcustomer')

@login_required(login_url='signin')
@user_passes_test(is_admin)  # Only admin can add employees
def addMaterial(request):
    if request.method == "POST":
        material_name = request.POST['name']
        material_make = request.POST['material_make']
        material_size_in_meters = request.POST['material_size_in_meter']
        material_size_in_feet = request.POST['material_size_in_feet']
        additional_info = request.POST['additiona_info']
        # Generate Material_Id starting with jremp0001 and display in back-end
        last_material = MaterialMaster.objects.order_by('-Material_Id').first()
        if last_material:
            last_id = int(last_material.Material_Id[3:])  # Extract the numeric part
            new_id = f"MAT{last_id + 1:04d}"
        else:
            new_id = "MAT0001"
        context = {'data':new_id}
        MaterialMaster.objects.create(Material_Id = new_id, Material_Name = material_name, Material_Make = material_make, Material_Size_In_Meters = material_size_in_meters, Material_Size_In_Feet = material_size_in_feet, Additional_Info = additional_info)
        return redirect('listmaterial')
        


    # Generate Material_Id starting with jremp0001 and display in front-end 
    last_material = MaterialMaster.objects.order_by('-Material_Id').first()
    if last_material:
        last_id = int(last_material.Material_Id[3:])  # Extract the numeric part
        new_id = f"MAT{last_id + 1:04d}"
    else:
        new_id = "MAT0001"
    context = {'data':new_id}
    return render(request,'add_material.html',context)

@login_required(login_url='signin')
@user_passes_test(is_admin)  # Only admin can add employees
def listMaterial(request):
    data = MaterialMaster.objects.filter(Status = 1)
    context = {'data':data}
    return render(request,'list_material.html',context)

@login_required(login_url='signin')
@user_passes_test(is_admin)  # Only admin can add employees
def editMaterial(request,id):
    if request.method == "POST":
        material_name = request.POST['name']
        material_make = request.POST['material_make']
        material_size_in_meters = request.POST['material_size_in_meter']
        material_size_in_feet = request.POST['material_size_in_feet']
        additional_info = request.POST['additiona_info']
        MaterialMaster.objects.filter(Material_Id = id).update(Material_Name = material_name, Material_Make = material_make, Material_Size_In_Meters = material_size_in_meters, Material_Size_In_Feet = material_size_in_feet, Additional_Info = additional_info)
        return redirect('listmaterial')
    data = MaterialMaster.objects.filter(Material_Id = id , Status =1)
    context = {'data':data}
    return render(request,'edit_material.html',context)

@login_required(login_url='signin')
@user_passes_test(is_admin)  # Only admin can add employees
def materialDetails(request,id):
    data = MaterialMaster.objects.filter(Material_Id = id , Status =1)
    context = {'data':data}
    return render(request,'material_details.html',context)

@login_required(login_url='signin')
@user_passes_test(is_admin)  # Only admin can add employees
def deleteMaterial(request,id):
    MaterialMaster.objects.filter(Material_Id = id).update(Status = 0)
    return redirect('listmaterial')


@login_required(login_url='signin')
@user_passes_test(is_admin)  # Only admin can add employees
def addInward(request, id):
    if request.method == 'POST':
        material_id = request.POST['material_id']
        vendor_name = request.POST['vendor_name']
        vendor_phone = request.POST['vendor_phone']
        vendor_gst = request.POST['vendor_gst']
        invoice_cost = request.POST['invoice_cost']
        invoice_quantity = request.POST['invoice_quantity']
        batch_no = request.POST['batch_no']
        additional_info = request.POST['additional_info']


        last_Sno = InwardMaster.objects.last()  # Get the last entry

        if last_Sno:  
            new_sno = last_Sno.S_No + 1  # Assuming 'Sno' is the integer field storing serial numbers
        else:
            new_sno = 1  # Start from 1 if no records exist


        # Generate Inward_Id starting with INW0001 and store in back-end 
        last_inward = InwardMaster.objects.order_by('-Inward_Id').first()
        if last_inward:
            last_id = int(last_inward.Inward_Id[3:])  # Extract the numeric part
            new_inw_id = f"INW{last_id + 1:04d}"
        else:
            new_inw_id = "INW0001"

        # Generate Batch_Id starting with BAT0001 and store in back-end 
        last_batch = InwardMaster.objects.order_by('-Batch_Id').first()
        if last_batch:
            last_id = int(last_batch.Batch_Id[3:])  # Extract the numeric part
            new_bat_id = f"BAT{last_id + 1:04d}"
        else:
            new_bat_id = "BAT0001"


        Material = MaterialMaster.objects.filter(Material_Id = material_id, Status = 1)
        if Material:
            InwardMaster.objects.create(S_No = new_sno, Inward_Id = new_inw_id, Material_Id = material_id, Vendor_Name = vendor_name, Vendor_Mobile = vendor_phone, Vendor_GST = vendor_gst, Invoice_Cost = invoice_cost, Invoice_Quantity = invoice_quantity, Batch_No = batch_no, Batch_Id = new_bat_id, Additional_Info = additional_info)
        else:
            messages.info(request,"Material Id Not Available")
        return redirect('listinward')

    
    mat_id = MaterialMaster.objects.filter(Material_Id = id , Status =1)

    # Generate Inward_Id starting with INW0001 and display in front-end 
    last_inward = InwardMaster.objects.order_by('-Inward_Id').first()
    if last_inward:
        last_id = int(last_inward.Inward_Id[3:])  # Extract the numeric part
        new_inw_id = f"INW{last_id + 1:04d}"
    else:
        new_inw_id = "INW0001"

    # Generate Batch_Id starting with BAT0001 and display in front-end 
    last_batch = InwardMaster.objects.order_by('-Batch_Id').first()
    if last_batch:
        last_id = int(last_batch.Batch_Id[3:])  # Extract the numeric part
        new_bat_id = f"BAT{last_id + 1:04d}"
    else:
        new_bat_id = "BAT0001"

    context = {'mat_id':mat_id,'inw_id':new_inw_id,'bat_id':new_bat_id}
    
    return render(request,'add_inward.html', context)

@login_required(login_url='signin')
@user_passes_test(is_admin)  # Only admin can add employees
def listInward(request):
    data = InwardMaster.objects.filter(Status = 1)
    context = {'data':data}
    return render(request,'list_inward.html',context)

@login_required(login_url='signin')
@user_passes_test(is_admin)  # Only admin can add employees
def inwardDetails(request,id):
    data = InwardMaster.objects.filter(Inward_Id = id , Status =1)
    context = {'data':data}
    return render(request,'inward_details.html',context)



@login_required(login_url='signin')
@user_passes_test(is_admin)  # Only admin can add employees
def deleteInward(request,id):
    InwardMaster.objects.filter(Inward_Id = id).update(Status = 0)
    return redirect('listinward')



def city_autocomplete(request):
    return render(request, 'invoice.html')
    data = CustomerDetails.objects.filter(Status = 1)
    context = {'data':data}
    # Invoice.objects.create(invoice_number = 1, customer_name = "Test", date = "25-10-2001", total_amount = 1000)

    return render(request,'auto_complete.html', context)


def generate_invoice_pdf(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    html_string = render(request, 'invoice.html', {'invoice': invoice}).content.decode()
    pdf = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
    
    return response




@login_required(login_url='signin')
@user_passes_test(is_admin)  # Only admin can add employees
def addProduct(request):
    if request.method == 'POST':
        name = request.POST['name']
        gst = request.POST['gst']
        hsn = request.POST['hsn']
        last_product = ProductMaster.objects.order_by('-Product_Id').first()
        if last_product:
            last_id = int(last_product.Product_Id[4:])  # Extract the numeric part
            new_id = f"PROD{last_id + 1:04d}"
        else:
            new_id = "PROD0001"

        ProductMaster.objects.create(Product_Id = new_id, Product_Name = name, GST = gst, HSN_Code = hsn)

        return redirect('addproduct')
    
    last_product = ProductMaster.objects.order_by('-Product_Id').first()
    if last_product:
        last_id = int(last_product.Product_Id[4:])  # Extract the numeric part
        new_id = f"PROD{last_id + 1:04d}"
    else:
        new_id = "PROD0001"
    
    context = {'data':new_id}

    return render(request,'add_product.html',context)

@login_required(login_url='signin')
@user_passes_test(is_admin)  # Only admin can add employees
def listProduct(request):
    data = ProductMaster.objects.filter(Status = 1)
    context = {'data':data}
    return render(request,'list_product.html',context)





@login_required(login_url='signin')
@user_passes_test(is_admin)  # Only admin can add employees
def addCategories(request):
    CategoriesMaster.objects.filter(Product_Name = "Digital Print").update(Product_Name = "DIGITAL PRINT")
#     sizes = [
#     "3 x 2", "4 x 2", "4 x 3", "5 x 3", "6 x 3", "6 x 4", "7 x 4", "8 x 3",
#     "8 x 4", "8 x 5", "10 x 3", "10 x 4", "10 x 5"
# ]





#     product = "Digital Print"
#     Category = "VINYL"
#     subcategory = "ALPHA"

#     for s in sizes:
#         last_categories = CategoriesMaster.objects.order_by('-Categories_Id').first()
#         if last_categories:
#             last_id = int(last_categories.Categories_Id[3:])  # Extract the numeric part
#             new_id = f"CAT{last_id + 1:04d}"
#         else:
#             new_id = "CAT0001"
        
#         CategoriesMaster.objects.create(Categories_Id = new_id, Product_Name = product, Categories_Name = Category, Sub_Categories = subcategory, Size = s)

    
    if request.method == 'POST':
        product_name = request.POST['product_name']
        category_name = request.POST['category_name']
        sub_category = request.POST['sub_category']
        size = request.POST['size']
        
        last_categories = CategoriesMaster.objects.order_by('-Categories_Id').first()
        if last_categories:
            last_id = int(last_categories.Categories_Id[3:])  # Extract the numeric part
            new_id = f"CAT{last_id + 1:04d}"
        else:
            new_id = "CAT0001"
            
        CategoriesMaster.objects.create(Categories_Id = new_id, Product_Name = product_name, Categories_Name = category_name, Sub_Categories = sub_category, Size = size)

        return redirect('addcategories')

    last_categories = CategoriesMaster.objects.order_by('-Categories_Id').first()
    if last_categories:
        last_id = int(last_categories.Categories_Id[3:])  # Extract the numeric part
        new_id = f"CAT{last_id + 1:04d}"
    else:
        new_id = "CAT0001"

    products = ProductMaster.objects.filter(Status = 1)
    
    context = {'data':new_id, 'products':products}

    return render(request,'add_categories.html',context)

@login_required(login_url='signin')
@user_passes_test(is_admin)  # Only admin can add employees
def listCategories(request):
    data = CategoriesMaster.objects.filter(Status = 1)
    context = {'data':data}
    return render(request,'list_categories.html',context)


@login_required(login_url='signin')
@user_passes_test(is_admin)  # Only admin can add employees
def addCost(request):
    if request.method == "POST":
        product_name = request.POST['product_name']
        category_name = request.POST['category_name']
        sub_category = request.POST['sub_category']
        cost_calculate = request.POST['cost_calculate']
        cost = request.POST['cost']
        size = request.POST['size']

        last_product = CostMaster.objects.order_by('-Cost_Id').first()
        if last_product:
            last_id = int(last_product.Cost_Id[4:])  # Extract the numeric part
            new_id = f"COST{last_id + 1:04d}"
        else:
            new_id = "COST0001"

        if cost_calculate == "Cost Per Unit":
            CostMaster.objects.create(Cost_Id = new_id, Product_Name = product_name, Category_Name = category_name, Sub_Category = sub_category, Cost_Per_Unit_Status = 1, Cost_Per_Unit = cost, Size = size)
            return redirect('addcost')
        elif cost_calculate == "Fixed Cost":
            CostMaster.objects.create(Cost_Id = new_id, Product_Name = product_name, Category_Name = category_name, Sub_Category = sub_category, Fixed_Cost_Status = 1, Fixed_Cost = cost, Size = size)
            return redirect('addcost')
        else:
            CostMaster.objects.create(Cost_Id = new_id, Product_Name = product_name, Category_Name = category_name, Sub_Category = sub_category, Cost_Per_Sqft_Status = 1, Cost_Per_Sqft = cost, Size = size)
            return redirect('addcost')
        
    last_product = CostMaster.objects.order_by('-Cost_Id').first()
    if last_product:
        last_id = int(last_product.Cost_Id[4:])  # Extract the numeric part
        new_id = f"COST{last_id + 1:04d}"
    else:
        new_id = "COST0001"

    category = CategoriesMaster.objects.filter(Status = 1)
    products = ProductMaster.objects.filter(Status = 1)
        
    context = {'data':new_id, 'category':category, 'products':products}


    return render(request,'add_cost.html',context)

@login_required(login_url='signin')
@user_passes_test(is_admin)  # Only admin can add employees
def listCost(request):
    data = CostMaster.objects.filter(Status =1)
    context = {'data':data}
    return render(request,'list_cost.html',context)

@login_required(login_url='signin')
def bill(request):
    # for adding multiple form entry in db 
    if request.method == "POST":
        try:
            # Parse JSON data
            data = json.loads(request.body)
            entries = data.get("entries", [])
            # Save each entry into the database
            for entry in entries:
                last_bill = BillingMaster.objects.order_by('-Bill_Id').first()
                if last_bill:
                    last_id = int(last_bill.Bill_Id[4:])  # Extract the numeric part
                    new_id = f"BILL{last_id + 1:04d}"
                else:
                    new_id = "BILL0001"

                detail_id = BillingMaster.objects.create(
                    Bill_Id= new_id,
                    Customer_Id=data.get("customer_id"),
                    Customer_Name=data.get("customer_name"),
                    Phone_No=data.get("customer_phone"),
                    Grand_Total = int(data.get("grand_total", 0)) if data.get("grand_total") not in [None, "", "None"] else 0,
                    Grand_Total_With_Gst = 0,
                    Pending_Amount = int(data.get("grand_total", 0)) if data.get("grand_total") not in [None, "", "None"] else 0
                )
               

                break

            

            for entry in entries:
                last_bill = BillingDetails.objects.order_by('-Item_Id').first()
                if last_bill:
                    last_id = int(last_bill.Item_Id[12:])  # Extract the numeric part
                    new_id = f"ITM{last_id + 1:01d}-{detail_id}"
                else:
                    new_id = f"ITM1-{detail_id}"

                specification = entry.get("product", "NONE") if entry.get("product") not in [None, "", "None"] else "NONE"
                splitted_spec = specification.split(",")

                costs = entry.get("cost", "NONE") if entry.get("cost") not in [None, "", "None"] else "NONE"
                splitted_cost = costs.split("/")
                totalSqft=entry.get("dimension", 0) if entry.get("dimension") not in [None, "", "None"] else 0

                
                
                BillingDetails.objects.create(
                    Bill_Id= detail_id,
                    Item_Id= new_id,
                    Customer_Id=data.get("customer_id"),
                    Customer_Name=data.get("customer_name"),
                    Phone_No=data.get("customer_phone"),
                    Product_Name=splitted_spec[0] ,
                    Custom_Product=entry.get("custom", "NONE") if entry.get("custom") not in [None, "", "None"] else "NONE",
                    Category_Name=splitted_spec[1],
                    Sub_Category=splitted_spec[2],
                    Size = entry.get("size", "NONE") if entry.get("size") not in [None, "", "None"] else "NONE",
                    Length=int(entry.get("length", 0)) if entry.get("length") not in [None, "", "None"] else 0,
                    Width=int(entry.get("width", 0)) if entry.get("width") not in [None, "", "None"] else 0,
                    Total_Sqft=int(totalSqft[-1]),
                    Quantity=int(entry.get("quantity", 0)),  # Convert to int (default 0 if missing)
                    Cost_Per_Quantity=splitted_cost[0],
                    Modified_Cost = 0 if splitted_cost[1] == " None " else splitted_cost[1],
                    GST=float(entry.get("gst", 0)) if entry.get("gst") not in [None, "", "None"] else 0,  # Convert to float (default 0 if missing)
                    HSN_Code=entry.get("hsn", "NONE") if entry.get("hsn") not in [None, "", "None"] else "NONE",
                    Total_Cost=float(entry.get("total", 0)),  # Convert to float
                    Total_Cost_With_Gst=float(entry.get("total_with_gst", 0)),  # Convert to float
                    Remarks = entry.get("remarks", "NONE") if entry.get("remarks") not in [None, "", "None"] else "NONE",
                )
            return redirect("listbill")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            traceback.print_exc()  # This prints the full error traceback in the console
            return JsonResponse({"error": str(e)}, status=500)

    last_bill = BillingMaster.objects.order_by('-Bill_Id').first()
    if last_bill:
        last_id = int(last_bill.Bill_Id[4:])  # Extract the numeric part
        new_id = f"BILL{last_id + 1:04d}"
    else:
        new_id = "BILL0001"

    data = CustomerDetails.objects.filter(Status = 1)
    category = CategoriesMaster.objects.filter(Status = 1)
    products = ProductMaster.objects.filter(Status = 1)
    cos = CostMaster.objects.filter(Status = 1)
        
    context = {'new_id':new_id, 'category':category, 'products':products, 'data': data, 'cos': cos, 'new_id': new_id }

    
    return render(request,'bill.html',context)

@login_required(login_url='signin')
def listBill(request):
    data = BillingMaster.objects.filter(Status =1).order_by("-Bill_Id")
    context = {'data':data}
    return render(request,'list_bill.html',context)


@login_required(login_url='signin')
def billDetails(request,id):
    data = BillingDetails.objects.filter(Bill_Id = id , Status =1)
    data2 = BillingMaster.objects.get(Bill_Id = id , Status =1)
    context = {'data':data, 'data2':data2}
    return render(request,'bill_details.html',context)




@login_required(login_url='signin')
def quote(request):
    # for adding multiple form entry in db 
    if request.method == "POST":
        try:
            # Parse JSON data
            data = json.loads(request.body)
            entries = data.get("entries", [])
            # Save each entry into the database
            for entry in entries:
                last_bill = QuoteMaster.objects.order_by('-Quote_Id').first()
                if last_bill:
                    last_id = int(last_bill.Quote_Id[4:])  # Extract the numeric part
                    new_id = f"QUOT{last_id + 1:04d}"
                else:
                    new_id = "QUOT0001"
                detail_id = QuoteMaster.objects.create(
                    Quote_Id= new_id,
                    Customer_Id=data.get("customer_id"),
                    Customer_Name=data.get("customer_name"),
                    Phone_No=data.get("customer_phone"),
                    Grand_Total = int(data.get("grand_total", 0)) if data.get("grand_total") not in [None, "", "None"] else 0,
                    Grand_Total_With_Gst = int(data.get("grand_total_with_gst", 0)) if data.get("grand_total_with_gst") not in [None, "", "None"] else 0,
                )
                break
            for entry in entries:
                last_bill = QuoteDetails.objects.order_by('-Item_Id').first()
                if last_bill:
                    last_id = int(last_bill.Item_Id[12:])  # Extract the numeric part
                    new_id = f"ITM{last_id + 1:01d}-{detail_id}"
                else:
                    new_id = f"ITM1-{detail_id}"
                QuoteDetails.objects.create(
                    Quote_Id= detail_id,
                    Item_Id= new_id,
                    Customer_Id=data.get("customer_id"),
                    Customer_Name=data.get("customer_name"),
                    Phone_No=data.get("customer_phone"),
                    Product_Name=entry.get("product", "NONE") if entry.get("product") not in [None, "", "None"] else "NONE",
                    Custom_Product=entry.get("custom", "NONE") if entry.get("custom") not in [None, "", "None"] else "NONE",
                    Category_Name=entry.get("category", "NONE") if entry.get("category") not in [None, "", "None"] else "NONE",
                    Sub_Category=entry.get("sub_category", "NONE") if entry.get("sub_category") not in [None, "", "None"] else "NONE",
                    Length=int(entry.get("length", 0)) if entry.get("length") not in [None, "", "None"] else 0,
                    Width=int(entry.get("width", 0)) if entry.get("width") not in [None, "", "None"] else 0,
                    Total_Sqft=int(entry.get("total_sqft", 0)) if entry.get("total_sqft") not in [None, "", "None"] else 0,
                    Quantity=int(entry.get("quantity", 0)),  # Convert to int (default 0 if missing)
                    Cost_Per_Quantity=float(entry.get("cost", 0)) if entry.get("cost") not in [None, "", "None"] else 0,  # Convert to float (default 0 if missing)
                    GST=float(entry.get("gst", 0)) if entry.get("gst") not in [None, "", "None"] else 0,  # Convert to float (default 0 if missing)
                    HSN_Code=entry.get("hsn", "NONE") if entry.get("hsn") not in [None, "", "None"] else "NONE",
                    Total_Cost=float(entry.get("total", 0)),  # Convert to float
                    Total_Cost_With_Gst=float(entry.get("total_with_gst", 0))  # Convert to float
                )
            return redirect("listquote")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            traceback.print_exc()  # This prints the full error traceback in the console
            return JsonResponse({"error": str(e)}, status=500)
    return redirect('listquote')

@login_required(login_url='signin')
def listQuote(request):
    data = QuoteMaster.objects.filter(Status =1)
    context = {'data':data}
    return render(request,'list_quote.html',context)

@login_required(login_url='signin')
def quoteDetails(request,id):
    data = QuoteDetails.objects.filter(Quote_Id = id , Status =1)
    data2 = QuoteMaster.objects.get(Quote_Id = id , Status =1)
    context = {'data':data, 'data2':data2}
    return render(request,'quote_details.html',context)


@login_required(login_url='signin')
def estimate(request):

    # for adding multiple form entry in db 
    if request.method == "POST":
        try:
            # Parse JSON data
            data = json.loads(request.body)
            entries = data.get("entries", [])
            # Save each entry into the database
            for entry in entries:
                last_bill = EstimateMaster.objects.order_by('-Estimation_Id').first()
                if last_bill:
                    last_id = int(last_bill.Estimation_Id[4:])  # Extract the numeric part
                    new_id = f"ESTM{last_id + 1:04d}"
                else:
                    new_id = "ESTM0001"
                detail_id = EstimateMaster.objects.create(
                    Estimation_Id= new_id,
                    Customer_Id=data.get("customer_id"),
                    Customer_Name=data.get("customer_name"),
                    Phone_No=data.get("customer_phone"),
                    Grand_Total = int(data.get("grand_total", 0)) if data.get("grand_total") not in [None, "", "None"] else 0,
                    # Grand_Total_With_Gst = int(data.get("grand_total_with_gst", 0)) if data.get("grand_total_with_gst") not in [None, "", "None"] else 0,
                )
                break
            for entry in entries:
                last_bill = EstimateDetails.objects.order_by('-Item_Id').first()
                if last_bill:
                    last_id = int(last_bill.Item_Id[12:])  # Extract the numeric part
                    new_id = f"ITM{last_id + 1:01d}-{detail_id}"
                else:
                    new_id = f"ITM1-{detail_id}"
                EstimateDetails.objects.create(
                    Estimation_Id = detail_id,
                    Item_Id= new_id,
                    Customer_Id=data.get("customer_id"),
                    Customer_Name=data.get("customer_name"),
                    Phone_No=data.get("customer_phone"),
                    Product_Name=entry.get("product", "NONE") if entry.get("product") not in [None, "", "None"] else "NONE",
                    Custom_Product=entry.get("custom", "NONE") if entry.get("custom") not in [None, "", "None"] else "NONE",
                    Category_Name=entry.get("category", "NONE") if entry.get("category") not in [None, "", "None"] else "NONE",
                    Sub_Category=entry.get("sub_category", "NONE") if entry.get("sub_category") not in [None, "", "None"] else "NONE",
                    Length=int(entry.get("length", 0)) if entry.get("length") not in [None, "", "None"] else 0,
                    Width=int(entry.get("width", 0)) if entry.get("width") not in [None, "", "None"] else 0,
                    Total_Sqft=int(entry.get("total_sqft", 0)) if entry.get("total_sqft") not in [None, "", "None"] else 0,
                    Quantity=int(entry.get("quantity", 0)),  # Convert to int (default 0 if missing)
                    Cost_Per_Quantity=float(entry.get("cost", 0)) if entry.get("cost") not in [None, "", "None"] else 0,  # Convert to float (default 0 if missing)
                    # GST=float(entry.get("gst", 0)) if entry.get("gst") not in [None, "", "None"] else 0,  # Convert to float (default 0 if missing)
                    # HSN_Code=entry.get("hsn", "NONE") if entry.get("hsn") not in [None, "", "None"] else "NONE",
                    Total_Cost=float(entry.get("total", 0)),  # Convert to float
                    # Total_Cost_With_Gst=float(entry.get("total_with_gst", 0))  # Convert to float
                )
            return redirect("listestimate")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            traceback.print_exc()  # This prints the full error traceback in the console
            return JsonResponse({"error": str(e)}, status=500)
  
    return redirect('bill')

@login_required(login_url='signin')
def listEstimate(request):
    data = EstimateMaster.objects.filter(Status =1)
    context = {'data':data}
    return render(request,'list_estimate.html',context)
@login_required(login_url='signin')
def estimateDetails(request,id):
    data = EstimateDetails.objects.filter(Estimation_Id = id , Status =1)
    data2 = EstimateMaster.objects.get(Estimation_Id = id , Status =1)
    context = {'data':data, 'data2':data2}
    return render(request,'estimate_details.html',context)




 

@login_required(login_url='signin')
@user_passes_test(is_admin)  # Only admin can add employees
def add_employee(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        emp_id = request.POST['emp_id']
        name = request.POST['name']
        phone = request.POST['phone']
        DOJ = request.POST['DOJ']
        blood_group = request.POST['blood_group']
        aadhar = request.POST['aadhar']
        pan = request.POST['pan']
        email = request.POST['email']
        role = request.POST['role']
        address = request.POST['address']

        # Create employee user
        user = Employee.objects.create(
            username=username,
            password=make_password(password),  # Hashing the password
            emp_id=emp_id,
            first_name=name,  # Django default field
            phone=phone,
            DOJ=DOJ,
            blood_group=blood_group,
            aadhar=aadhar,
            pan=pan,
            email=email,
            address=address,
            role=role  # Default role as Employee
        )
        messages.info(request,"employee added")
        return redirect('addemployee')  # Redirect after successful creation
    last_emp = Employee.objects.order_by('-emp_id').first()
    if last_emp.emp_id:
        last_emp = int(last_emp.emp_id[3:])  # Extract the numeric part
        new_id = f"EMP{last_emp + 1:04d}"
    else:
        new_id = "EMP0001"
    context = {'data':new_id}

    return render(request, 'add_employee.html', context)

@login_required(login_url='signin')
@user_passes_test(is_admin)  # Only admin can add employees
def list_employee(request):
    data = Employee.objects.all()
    context = {'data':data}
 
   
    return render(request,'list_employee.html',context)

@login_required(login_url='signin')
def invoice(request,id):
    splitted_billId = id.split("-")
    billId = splitted_billId[0]
    if id.startswith("BILL"):
        data = BillingDetails.objects.filter(Bill_Id = billId , Status =1)
        data2 = BillingMaster.objects.get(Bill_Id = billId , Status =1)
        data3 = CustomerDetails.objects.get(Customer_Id = data2.Customer_Id)
        data4 = Payment_Master.objects.filter(Payment_Id=id)
        data5 = Payment_Details.objects.filter(Payment_Id=id)
        current_date = datetime.today()
        context = {'data':data, 'data2':data2,'data3':data3,'current_date':current_date,'data4':data4,'billId':billId,'invoice_no':id,'data5':data5}
        return render(request,'invoice.html',context)
    elif id.startswith("ESTM"):
        data = EstimateDetails.objects.filter(Estimation_Id = id , Status =1)
        data2 = EstimateMaster.objects.get(Estimation_Id = id , Status =1)
        data3 = CustomerDetails.objects.get(Customer_Id = data2.Customer_Id)
        current_date=datetime.today()
        context = {'data':data, 'data2':data2,'data3':data3,'current_date':current_date}
        return render(request,'invoive_no_gst.html',context)
    elif id.startswith("QUOT"):
        data = QuoteDetails.objects.filter(Quote_Id = id , Status =1)
        data2 = QuoteMaster.objects.get(Quote_Id = id , Status =1)
        data3 = CustomerDetails.objects.get(Customer_Id = data2.Customer_Id)
        current_date=datetime.today()
        context = {'data':data, 'data2':data2,'data3':data3,'current_date':current_date}
        return render(request,'invoice_quote.html',context)
    return redirect('bill')


@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect("signin")


@login_required(login_url='signin')
def add_payment(request, id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Load request data once
            table_data = data.get("tableData", [])
            last_pay = Payment_Master.objects.filter(Payment_Id__startswith=id).order_by('-Payment_Id').first()
            
            if last_pay:
                # Extract the numeric part after 'PAY'
                last_pay_id = int(last_pay.Payment_Id.split("PAY")[-1])  # Extract number after "PAY"
                new_pay_id = f"{last_pay.Payment_Id[:-len(str(last_pay_id))]}{last_pay_id + 1}"  # Increment
            else:
                new_pay_id = f"{id}"


            
            print("======+++++")

            paym_id = Payment_Master.objects.create(
                Payment_Id=new_pay_id,
                Bill_Id = id,
                Grand_Total=int(float(data.get("totalAmount") or 0)),  # Ensure it's never None
                Paid_Amount=int(float((data.get("totalAmount") or 0)) - int(float((data.get("finalPending") or 0)))),
                Pending_Amount=int(float(data.get("finalPending") or 0)), 
                
            )

            BillingMaster.objects.filter(Bill_Id = id.split("-")[0]).update(
                Fully_Paid=1 if data.get("finalPending") == "0.00" else 0,  # Fully paid if no pending amount
                Partialy_Paid=1 if 0 < int(float((data.get("finalPending") or 0))) < int(float((data.get("totalAmount") or 0))) else 0,  # Partial payment
                Not_Paid=1 if (data.get("totalAmount") or 0) == (data.get("finalPending") or 0) else 0,  # Not paid if pending = total
                Paid_Amount = int(float(data.get("totalAmount"))) - int(float(data.get("finalPending"))),
                Pending_Amount = int(float(data.get("finalPending")))
                )
                
            for entry in table_data:
                print(type(entry.get("pending_amount")))

                Payment_Details.objects.create(
                    Payment_Id=paym_id,
                    Grand_Total=int(float(data.get("totalAmount") or 0)),  # Ensure it's never None
                    Paid_Amount=int(float(entry.get("amount"))),  # Avoid NoneType subtraction
                    Pending_Amount=int(float(data.get("pending_amount") or 0)),   # Ensure correct pending amount
                    Payment_Mode=entry.get("payment_mode"),
                    Utr_Or_Reason=entry.get("utr_reason"),
                    Mobile_No=entry.get("mobile_number"),
                    Bill_Id = id.split("-")[0]
                    
                )
                if entry.get("payment_mode") == "MANUAL CLOSE":
                    BillingMaster.objects.filter(Bill_Id = id.split("-")[0]).update(
                    Force_Paid=1 if entry.get("payment_mode") == "MANUAL CLOSE" else 0,  # Set Force_Paid if MANUAL_CLOSE
                    )



            
            return JsonResponse({"message": "Data received successfully"}, status=200)


        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)  # Use 400 for bad requests
        
    
 
    last_pay = Payment_Master.objects.filter(Payment_Id__startswith=id).order_by('-Payment_Id').first()  

    if last_pay:
        # Extract the numeric part after 'PAY'
        last_pay_id = int(last_pay.Payment_Id.split("PAY")[-1])  # Extract number after "PAY"
        new_pay_id = f"{last_pay.Payment_Id[:-len(str(last_pay_id))]}{last_pay_id + 1}"  # Increment
        data= Payment_Master.objects.filter(Payment_Id__startswith=id).last()
    else:
        new_pay_id = f"{id}-PAY1"
        data =  BillingMaster.objects.filter(Bill_Id=id).last()

    # Handle GET request (Fetch data for the given Bill_Id)
    
    context = {'data': data,'new_pay_id' : new_pay_id}
    return render(request, "add_payment.html", context)

@login_required(login_url='signin')
def list_payment(request,id):
    data = Payment_Master.objects.filter(Payment_Id__startswith=id)
    context = {'data':data}
    return render(request,'list_payments.html',context)




@login_required(login_url='signin')
def bill_and_pay(request,id):
    # for adding multiple form entry in db 
    if request.method == "POST":
        try:
            # Parse JSON data
            data = json.loads(request.body)
            entries = data.get("entries", [])
            # Save each entry into the database
            for entry in entries:
                last_bill = BillingMaster.objects.order_by('-Bill_Id').first()
                if last_bill:
                    last_id = int(last_bill.Bill_Id[4:])  # Extract the numeric part
                    new_id = f"BILL{last_id + 1:04d}"
                else:
                    new_id = "BILL0001"

                detail_id = BillingMaster.objects.create(
                    Bill_Id= new_id,
                    Customer_Id=data.get("customer_id"),
                    Customer_Name=data.get("customer_name"),
                    Phone_No=data.get("customer_phone"),
                    Grand_Total = int(data.get("grand_total", 0)) if data.get("grand_total") not in [None, "", "None"] else 0,
                    Grand_Total_With_Gst = 0,

                )
               

                break

            

            for entry in entries:
                last_bill = BillingDetails.objects.order_by('-Item_Id').first()
                if last_bill:
                    last_id = int(last_bill.Item_Id[12:])  # Extract the numeric part
                    new_id = f"ITM{last_id + 1:01d}-{detail_id}"
                else:
                    new_id = f"ITM1-{detail_id}"

                specification = entry.get("product", "NONE") if entry.get("product") not in [None, "", "None"] else "NONE"
                splitted_spec = specification.split(",")

                costs = entry.get("cost", "NONE") if entry.get("cost") not in [None, "", "None"] else "NONE"
                splitted_cost = costs.split("/")
                totalSqft=entry.get("dimension", 0) if entry.get("dimension") not in [None, "", "None"] else 0

                
                
                BillingDetails.objects.create(
                    Bill_Id= detail_id,
                    Item_Id= new_id,
                    Customer_Id=data.get("customer_id"),
                    Customer_Name=data.get("customer_name"),
                    Phone_No=data.get("customer_phone"),
                    Product_Name=splitted_spec[0] ,
                    Custom_Product=entry.get("custom", "NONE") if entry.get("custom") not in [None, "", "None"] else "NONE",
                    Category_Name=splitted_spec[1],
                    Sub_Category=splitted_spec[2],
                    Size = entry.get("size", "NONE") if entry.get("size") not in [None, "", "None"] else "NONE",
                    Length=int(entry.get("length", 0)) if entry.get("length") not in [None, "", "None"] else 0,
                    Width=int(entry.get("width", 0)) if entry.get("width") not in [None, "", "None"] else 0,
                    Total_Sqft=int(totalSqft[-1]),
                    Quantity=int(entry.get("quantity", 0)),  # Convert to int (default 0 if missing)
                    Cost_Per_Quantity=splitted_cost[0],
                    Modified_Cost = 0 if splitted_cost[1] == " None " else splitted_cost[1],
                    GST=float(entry.get("gst", 0)) if entry.get("gst") not in [None, "", "None"] else 0,  # Convert to float (default 0 if missing)
                    HSN_Code=entry.get("hsn", "NONE") if entry.get("hsn") not in [None, "", "None"] else "NONE",
                    Total_Cost=float(entry.get("total", 0)),  # Convert to float
                    Total_Cost_With_Gst=float(entry.get("total_with_gst", 0)),  # Convert to float
                    Remarks = entry.get("remarks", "NONE") if entry.get("remarks") not in [None, "", "None"] else "NONE",
                )
            return redirect("addpayment", id=id)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            traceback.print_exc()  # This prints the full error traceback in the console
            return JsonResponse({"error": str(e)}, status=500)

    last_bill = BillingMaster.objects.order_by('-Bill_Id').first()
    if last_bill:
        last_id = int(last_bill.Bill_Id[4:])  # Extract the numeric part
        new_id = f"BILL{last_id + 1:04d}"
    else:
        new_id = "BILL0001"

    data = CustomerDetails.objects.filter(Status = 1)
    category = CategoriesMaster.objects.filter(Status = 1)
    products = ProductMaster.objects.filter(Status = 1)
    cos = CostMaster.objects.filter(Status = 1)
        
    context = {'new_id':new_id, 'category':category, 'products':products, 'data': data, 'cos': cos, 'new_id': new_id }

    
    return render(request,'bill.html',context)



@csrf_exempt
def upload_pdf(request):
    if request.method == "POST" and request.FILES.get("pdf_file"):
        pdf_file = request.FILES["pdf_file"]
        whatsapp_number = request.POST.get("whatsapp_number")

        file_path = os.path.join("media", pdf_file.name)
        file_url = request.build_absolute_uri("/media/" + pdf_file.name)

        with default_storage.open(file_path, "wb") as destination:
            for chunk in pdf_file.chunks():
                destination.write(chunk)

        response = send_pdf_whatsapp(whatsapp_number, file_url)
        return JsonResponse(response)

    return JsonResponse({"error": "Invalid request"}, status=400)

def send_pdf_whatsapp(to_number, pdf_url):
    access_token = "your_access_token"
    phone_number_id = "your_phone_number_id"

    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "document",
        "document": {
            "link": pdf_url,
            "filename": "invoice.pdf"
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()



def overall_invoice(request,id):
    
    data = BillingDetails.objects.filter(Bill_Id = id , Status =1)
    data2 = BillingMaster.objects.get(Bill_Id = id , Status =1)
    data3 = CustomerDetails.objects.get(Customer_Id = data2.Customer_Id)
    data4 = BillingMaster.objects.filter(Bill_Id=id)
    data5 = Payment_Details.objects.filter(Bill_Id=id)
    current_date = datetime.today()

    context = {'data':data, 'data2':data2,'data3':data3,'current_date':current_date,'data4':data4,'billId':id,'invoice_no':id,'data5':data5}
    return render(request,'overall_invoice.html',context)



def list_payments_terms(request,id):
    data=Payment_Details.objects.filter(Payment_Id = id)
    for i in data:
        print("00000",i.Paid_Amount)
    context ={'data':data}
    return render(request,'list_payment_terms.html',context)
    pass