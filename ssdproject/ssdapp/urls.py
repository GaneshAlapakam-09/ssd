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
    path('autocomplete/',views.city_autocomplete,name='autocomplete'),
]
