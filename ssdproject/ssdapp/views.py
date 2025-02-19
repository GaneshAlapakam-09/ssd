from django.shortcuts import render,redirect
from ssdapp.models import CustomerMaster,CustomerDetails,MaterialMaster,InwardMaster,Invoice,ProductMaster,CategoriesMaster,CostMaster,BillingMaster
from django.contrib import messages

from django.http import HttpResponse
from weasyprint import HTML

# Create your views here.

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

def listCustomer(request):
    data = CustomerDetails.objects.filter(Status = 1)
    context = {'data':data}
    return render(request,'list_customer.html',context)


def customerDetails(request,id):
    data = CustomerDetails.objects.filter(Customer_Id = id , Status =1)
    context = {'data':data}
    return render(request,'customer_details.html',context)


# def editCustomer_S(request):
#     data = CustomerDetails.objects.filter(Status=1)
#     context = {'data':data}
#     return render(request,'edit_customer_s.html',context)

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

def deleteCustomer(request,id):
    CustomerDetails.objects.filter(Customer_Id = id).update(Status = 0)
    CustomerMaster.objects.filter(Customer_Id = id).update(Status = 0)
    return redirect('listcustomer')


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


def listMaterial(request):
    data = MaterialMaster.objects.filter(Status = 1)
    context = {'data':data}
    return render(request,'list_material.html',context)


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


def materialDetails(request,id):
    data = MaterialMaster.objects.filter(Material_Id = id , Status =1)
    context = {'data':data}
    return render(request,'material_details.html',context)


def deleteMaterial(request,id):
    MaterialMaster.objects.filter(Material_Id = id).update(Status = 0)
    return redirect('listmaterial')



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


def listInward(request):
    data = InwardMaster.objects.filter(Status = 1)
    context = {'data':data}
    return render(request,'list_inward.html',context)

def inwardDetails(request,id):
    data = InwardMaster.objects.filter(Inward_Id = id , Status =1)
    context = {'data':data}
    return render(request,'inward_details.html',context)


def deleteInward(request,id):
    InwardMaster.objects.filter(Inward_Id = id).update(Status = 0)
    return redirect('listinward')



def city_autocomplete(request):
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


def listProduct(request):
    data = ProductMaster.objects.filter(Status = 1)
    context = {'data':data}
    return render(request,'list_product.html',context)






def addCategories(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        category_name = request.POST['category_name']
        sub_category = request.POST['sub_category']
        
        last_categories = CategoriesMaster.objects.order_by('-Categories_Id').first()
        if last_categories:
            last_id = int(last_categories.Categories_Id[3:])  # Extract the numeric part
            new_id = f"CAT{last_id + 1:04d}"
        else:
            new_id = "CAT0001"
            
        CategoriesMaster.objects.create(Categories_Id = new_id, Product_Name = product_name, Categories_Name = category_name, Sub_Categories = sub_category)

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


def listCategories(request):
    data = CategoriesMaster.objects.filter(Status = 1)
    context = {'data':data}
    return render(request,'list_categories.html',context)



def addCost(request):
    if request.method == "POST":
        product_name = request.POST['product_name']
        category_name = request.POST['category_name']
        sub_category = request.POST['sub_category']
        cost_calculate = request.POST['cost_calculate']
        cost = request.POST['cost']

        last_product = CostMaster.objects.order_by('-Cost_Id').first()
        if last_product:
            last_id = int(last_product.Cost_Id[4:])  # Extract the numeric part
            new_id = f"COST{last_id + 1:04d}"
        else:
            new_id = "COST0001"

        if cost_calculate == "Cost Per Unit":
            CostMaster.objects.create(Cost_Id = new_id, Product_Name = product_name, Category_Name = category_name, Sub_Category = sub_category, Cost_Per_Unit_Status = 1, Cost_Per_Unit = cost)
            return redirect('addcost')
        else:
            CostMaster.objects.create(Cost_Id = new_id, Product_Name = product_name, Category_Name = category_name, Sub_Category = sub_category, Cost_Per_Sqft_Status = 1, Cost_Per_Sqft = cost)
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


def listCost(request):
    data = CostMaster.objects.filter(Status =1)
    context = {'data':data}
    return render(request,'list_cost.html',context)


def bill(request):
    if request.method == "POST":
        customer_details = request.POST['customer_hidden']
        splitted_details = customer_details.strip().split("--")
        customer_id = splitted_details[0]
        customer_name = splitted_details[1]
        customer_phone = splitted_details[2]
        product_name = request.POST['product_name']
        category_name = request.POST['category_name']
        sub_category = request.POST['sub_category']
        quantity = request.POST['quantity']
        cost = request.POST['cost']
        gst = request.POST['gst']
        hsn = request.POST['hsn']
        total = request.POST['total']
        total_with_gst = request.POST['total_with_gst']
        last_bill = BillingMaster.objects.order_by('-Bill_Id').first()
        if last_bill:
            last_id = int(last_bill.Bill_Id[4:])  # Extract the numeric part
            new_id = f"BILL{last_id + 1:04d}"
        else:
            new_id = "BILL0001"
        if request.POST['length']:
            length = request.POST['length']
            width = request.POST['width']
            BillingMaster.objects.create(Bill_Id = new_id, Customer_Id = customer_id, Customer_Name = customer_name, Phone_No = customer_phone,Product_Name = product_name, Category_Name = category_name, Sub_Category = sub_category, Length = length, Width = width, Quantity = quantity, Cost_Per_Quantity = cost, GST = gst, HSN_Code = hsn, Total_Cost = total, Total_Cost_With_Gst = total_with_gst)
            return redirect('bill')
        else:
            BillingMaster.objects.create(Bill_Id = new_id, Customer_Id = customer_id, Customer_Name = customer_name, Phone_No = customer_phone,Product_Name = product_name, Category_Name = category_name, Sub_Category = sub_category, Quantity = quantity, Cost_Per_Quantity = cost, GST = gst, HSN_Code = hsn, Total_Cost = total, Total_Cost_With_Gst = total_with_gst)
            return redirect('bill')





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