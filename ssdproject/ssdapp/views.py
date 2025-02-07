from django.shortcuts import render,redirect
from ssdapp.models import CustomerMaster,CustomerDetails,MaterialMaster,InwardMaster,City
from django.contrib import messages
from django.http import JsonResponse

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

        CustomerMaster.objects.create(Customer_Id = new_id, Customer_Name = name, Phone_No = phone)
        CustomerDetails.objects.create(Customer_Id = new_id, Customer_Name = name, Phone_No = phone, Alt_Phone = altPhone, Email = email, Address = address)
        messages.info(request,"Form Submitted")

        return redirect('listcustomer')

        

    last_customer = CustomerMaster.objects.order_by('-Customer_Id').first()
    if last_customer:
        last_id = int(last_customer.Customer_Id[4:])  # Extract the numeric part
        new_id = f"SSDC{last_id + 1:04d}"
    else:
        new_id = "SSDC0001"
    
    context = {'data':new_id}

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
            CustomerDetails.objects.filter(Customer_Id=customerId).update(Customer_Name = name, Phone_No = phone, Alt_Phone = altPhone, Email = email, Address = address)
            return redirect('listcustomer')

    data = CustomerDetails.objects.filter(Customer_Id = id , Status =1)
    context = {'data':data}
    return render(request,'edit_customer.html',context)

def deleteCustomer(request,id):
    CustomerDetails.objects.filter(Customer_Id = id).delete()
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
    MaterialMaster.objects.filter(Material_Id = id).delete()
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


        # Generate S.no
        last_Sno = InwardMaster.objects.order_by('-S_No').first()
        if last_Sno:
            new_sno = last_Sno + 1
        else:
            new_sno = 1
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
        return render(request,'add_inward.html')

    
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


def city_autocomplete(request):


    return render(request,'auto_complete.html')