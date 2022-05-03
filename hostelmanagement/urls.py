from django.urls import path
from . import views
from hostelmanagement.forms import LoginForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",views.Home.as_view(),name="home"),
    path("hostel/<slug:slug>",views.SingleHostelView.as_view(),name="hostel_details"),
    path("areas/<slug:data>",views.areas_info,name="areadata"),
    path("search/",views.searchRes,name="search"),

    path("register/",views.UserRegisterView.as_view(),name="userRegister"),
    path("accounts/login/",auth_views.LoginView.as_view(template_name="hostelmanagement/Auth/login.html",authentication_form=LoginForm),name='login'),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'),name="logout"),
    path('login_success/', views.login_success, name='login_success'),

    # -----------------DASHBOARD------------------

    path("dashboard/",views.Dashboard.as_view(),name="dashboard"),

    path("dashboard/manage-hostel/",views.manageHostels,name="manage-hostels"),
    path("dashboard/manage-hostel/add",views.addHostel,name="add-hostel"),
    path("dashboard/manage-hostel/<str:pk>",views.hostelsUpdate,name="hostels-update"),
    path("dashboard/manage-hostel/delete/<str:pk>",views.hostelsDelete,name="hostels-delete"),

    path("dashboard/rooms/",views.rooms,name="rooms"),
    path("dashboard/rooms/add",views.addRoom,name="add-room"),
    path("dashboard/rooms/<str:pk>/",views.roomsUpdate,name="room-update"),
    path("dashboard/rooms/delete/<str:pk>/",views.roomsDelete,name="room-delete"),

    path("dashboard/hostel-details/",views.hostelDetails,name="hostel-details"),
    path("dashboard/hostel-details/add",views.addDetails,name="add-details"),
    path("dashboard/hostel-details/<str:pk>",views.hostelDetailsUpdate,name="hostelDetails-update"),
    path("dashboard/hostel-details/delete/<str:pk>",views.hostelDetailsDelete,name="hostelDetails-delete"),

    path("dashboard/facilities/",views.facilities,name="facilities"),
    path("dashboard/facilities/add",views.addFacility,name="add-facility"),
    path("dashboard/facilities/<str:pk>",views.facilitiesUpdate,name="facility-update"),
    path("dashboard/facilities/delete/<str:pk>",views.facilitiesDelete,name="facility-delete"),

    path("dashboard/profile/",views.ownerProfile,name="profile")

    #-----------------END DASHBOARD-----------------
]
