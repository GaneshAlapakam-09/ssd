from django.urls import path
from ssdapp import views

urlpatterns = [
    path('addcustomer/',views.addCustomer,name='addcustomer'),
    path('listcustomer/',views.listCustomer,name='listcustomer'),
    path('customerdetails/<str:id>',views.customerDetails,name='customerdetails'),
    path('editcustomer/<str:id>',views.editCustomer,name='editcustomer'),
    path('deletecustomer/<str:id>',views.deleteCustomer,name='deletecustomer'),
    path('addmaterial/',views.addMaterial,name='addmaterial'),
    path('listmaterial/',views.listMaterial,name='listmaterial'),
    path('editmaterial/<str:id>',views.editMaterial,name='editmaterial'),
    path('materialdetails/<str:id>',views.materialDetails,name='materialdetails'),
    path('deletematerial/<str:id>',views.deleteMaterial,name='deletematerial'),
    path('addinward/<str:id>',views.addInward,name='addinward'),
    path('listinward/',views.listInward,name='listinward'),
    path('inwarddetails/<str:id>',views.inwardDetails,name='inwarddetails'),
    path('deleteinward/<str:id>',views.deleteInward,name='deleteinward'),
    path('autocomplete/',views.city_autocomplete,name='autocomplete'),
    path('invoice/<int:invoice_id>/pdf/', views.generate_invoice_pdf, name='generate_invoice_pdf'),
    path('addproduct/',views.addProduct,name='addproduct'),
    path('listproduct/',views.listProduct,name='listproduct'),
    path('addcategories/',views.addCategories,name='addcategories'),
    path('listcategories/',views.listCategories,name='listcategories'),
    path('addcost/',views.addCost,name='addcost'),
    path('listcost/',views.listCost,name='listcost'),
    path('bill/',views.bill,name='bill'),
    path('quote/',views.quote,name='quote'),
    path('estimate/',views.estimate,name='estimate'),
    path('listbill/',views.listBill,name='listbill'),
    path('listquote/',views.listQuote,name='listquote'),
    path('listestimate/',views.listEstimate,name='listestimate'),
    path('billdetails/<str:id>',views.billDetails,name='billdetails'),
    path('quotedetails/<str:id>',views.quoteDetails,name='quotedetails'),
    path('estimatedetails/<str:id>',views.estimateDetails,name='estimatedetails'),
    path('addemployee/', views.add_employee, name='addemployee'),
    path('listemployee/', views.list_employee, name='listemployee'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('invoice/<str:id>', views.invoice, name='invoice'),
    path('', views.dashboard, name='dashboard'),
    path('addpayment/<str:id>', views.add_payment, name='addpayment'),
    path('listpayment/<str:id>', views.list_payment, name='listpayment'),
    path('bill_and_pay/<str:id>', views.bill_and_pay, name='bill_and_pay'),

     path('upload_pdf/', views.upload_pdf, name='upload_pdf'),





]


