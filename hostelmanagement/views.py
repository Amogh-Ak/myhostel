from django.shortcuts import render, redirect
from django.views import View
from .forms import FacilityForm, HostelDetailsForm, HostelForm, OwnerForm, RoomForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from hostelmanagement.models import Hostel, CustomUser, Room, Facilities, HostelDetail, OwnerDetail, Reviews
from django.views.generic import DetailView
from django.http.response import HttpResponseRedirect
from .filters import SearchFilter
from django.utils.text import slugify
from django.db.models import Q

# Create your views here.

def error_404_view(request, exception):
    return render(request,'404.html')

def error_500_view(request):
    return render(request,'500.html')

def login_success(request):
    """
    Redirects users based on whether they are in the admins group
    """
    print("SSS")
    print(request.user.is_Owner)
    if request.user.is_Owner == True:
        # user is an admin
        return redirect("dashboard")
    else:
        return redirect("home")

@login_required
def areas_info(request, data=None):
    if data == None:
        hostels = Hostel.objects.all()
    elif data == "Saptapur":
        hostels = Hostel.objects.filter(location=data)
    elif data == 'Malmaddi':
        hostels = Hostel.objects.filter(location=data)
    
    context = {
        "hostels":hostels,
        "area":data,
    }

    return render(request,"hostelmanagement/areaHostels.html",context)

@login_required
def explore(request):
    return render(request,"hostelmanagement/explore.html")

@login_required
def allhostels(request):
    hostels = Hostel.objects.all()
    return render(request,"hostelmanagement/allhostel.html",{"hostels":hostels})

class Home(View):
    def get(self, request):
        hostels = Hostel.objects.all()
        submitted = 'submitted' in request.GET
        data = request.GET if submitted else None
        
        searchFilter = SearchFilter(data, queryset=hostels)
        searchHostels = searchFilter.qs

        context = {
            'hostels':hostels,
            'searchHostels':searchHostels,
            'searchResult':searchFilter
        }
        return render(request, "hostelmanagement/home.html", context)

def searchRes(request):
    return render(request,"hostelmanagement/searchResult.html")

class UserRegisterView(View):

    def get(self,request):
        form = UserRegisterForm()
        context = {
            "form":form,
        }
    
        return render(request,"hostelmanagement/Auth/userRegister.html",context)

    def post(self,request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations! Registered Successfully')
            form.save()

        context = {
            "form":form,
        }
    
        return render(request,"hostelmanagement/Auth/userRegister.html",context)

class SingleHostelView(DetailView):
    def get(self, request, slug):
        hostel = Hostel.objects.get(slug=slug)
        hostel.views += 1
        hostel.save()
        owner = OwnerDetail.objects.get(usr=hostel.usr)
        context = {
            "hostel": hostel,
            "ownerDetail":owner,
            "reviews":hostel.reviews.all()
        }

        return render(request, "hostelmanagement/hostelDetail.html", context)

    def post(self, request, slug):
        hostel = Hostel.objects.get(slug=slug)
        if request.method == "POST":
            review = Reviews()
            review.text = request.POST.get("text")
            review.usr = request.user
            review.hostel = hostel

            review.save()
            return HttpResponseRedirect(request.path_info)
        hostel.views += 1
        hostel.save()
        owner = OwnerDetail.objects.get(usr=hostel.usr)
        context = {
            "hostel": hostel,
            "ownerDetail":owner,
            "reviews":hostel.reviews.all().order_by('-id')
        }

        return render(request, "hostelmanagement/hostelDetail.html", context)


class Dashboard(View):
    def get(self,request):
        facilities = Facilities.objects.all()
        rooms = Room.objects.filter(usr=request.user)
        
        try:
            owner = OwnerDetail.objects.get(usr=request.user)
        except OwnerDetail.DoesNotExist:
            owner = None
        data = Hostel.objects.filter(usr=request.user)
        dataList = list(data)
        obj_sample = {}
        list_sample = []
        # for value in dataList:
        #     res = len(list(Room.objects.filter(room_number = value.room.room_number)))
        #     obj_sample["rooms"] = res
        #     obj_sample["hostel"] = value.name
        #     list_sample.append(obj_sample)

        context = {
            "owner":owner,
            "data":data,
            "C_hostel":data,
            "C_rooms":rooms,
            "C_facilities":facilities
        }
        return render(request,"hostelmanagement/dashboard/ownerDashboard.html",context)

def manageHostels(request):
    if 'search-query' in request.GET:
        query = request.GET['search-query']
        searchData = Q(Q(name__icontains = query) | Q(location__icontains = query) | Q(type_of_hostel__icontains = query)  | Q(zipcode__icontains = query) | Q(status = "Approved"))
        data = Hostel.objects.filter(searchData)
    else:
        data = Hostel.objects.filter(usr=request.user)

    x = list(data)
    results = []
    for p in x:        
        if 'Approved' in p.status:
            results.append(p)   
    owner = OwnerDetail.objects.get(usr=request.user)
    print(owner)
    context ={
        "hostels":results,
        "owner":owner
    }
    return render(request,"hostelmanagement/dashboard/manageHostels.html",context)

def addHostel(request):
    hostelDetails = HostelDetail.objects.filter(usr=request.user)
    allfacilities = Facilities.objects.all()
    rooms = Room.objects.filter(usr=request.user)
    resFacility = []
    resRoom = []

    if request.method == "POST":
        form = HostelForm(request.POST, request.FILES) 
        Value1 = request.POST.get("details")
        facilitylist = request.POST.getlist("facilities")
        roomlist = request.POST.getlist("room")
        details = HostelDetail.objects.get(near_by=Value1)

        if form.is_valid():
            usr=request.user
            name = form.cleaned_data["name"]
            location = form.cleaned_data["location"]
            type_of_hostel = form.cleaned_data["type_of_hostel"]
            description = form.cleaned_data["description"]     
            images = form.cleaned_data["hostelimage"]
            food_facility = form.cleaned_data["food_facility"]
            zipcode = form.cleaned_data["zipcode"]
            slug = slugify(name)
            hostel = Hostel(usr=usr,name=name,details=details,slug=slug,location=location,zipcode=zipcode,type_of_hostel=type_of_hostel,description=description,images=images,food_facility=food_facility)
            messages.success(request,"Hostel has been added")
            hostel.save()

            for data in facilitylist:
                val = list(Facilities.objects.filter(facility=data))
                resFacility.append(val[0])                
            hostel.facilities.set(resFacility)
            
            for data in roomlist:
                val = list(Room.objects.filter(room_number=data))
                resRoom.append(val[0])
            hostel.room.set(resRoom)

            return HttpResponseRedirect(request.path_info)
        else:
            print(form.cleaned_data)
    else:
        form = HostelForm()
    owner = OwnerDetail.objects.get(usr=request.user)
    context = {
        "form":form,
        "hostelDetails":hostelDetails,
        "facilities":allfacilities,
        "rooms":rooms,
        "owner":owner
    }

    return render(request,"hostelmanagement/dashboard/Inserts/addHostels.html",context)

def hostelsUpdate(request, pk):
    room = Hostel.objects.get(id=pk)
    form = HostelForm(instance=room)


    if request.method == "POST":     
        form = HostelForm(request.POST, instance=room)
        
        if form.is_valid():
            room.save()
            return HttpResponseRedirect('/dashboard/manage-hostel/')
    else:
        form = HostelForm(instance=room)

    context = {
        "form":form,
    }

    return render(request,"hostelmanagement/dashboard/updates/hostelsUpdate.html",context)

def hostelsDelete(request, pk):
    data = Hostel.objects.get(id=pk)
    data.delete()
    return HttpResponseRedirect('/dashboard/manage-hostel/')

def rooms(request):
    hostels = Hostel.objects.filter(usr=request.user)
    
    if 'search-query' in request.GET:
        query = request.GET['search-query']
        print(query)
        data = Room.objects.filter(hostel_name=query)
    else:
        data = Room.objects.filter(usr=request.user)

    owner = OwnerDetail.objects.get(usr=request.user)
    context = {
        "rooms":data,
        "hostels":hostels,
        "owner":owner
    }

    return render(request,"hostelmanagement/dashboard/rooms.html",context)

def addRoom(request):
    if request.method == "POST":     
        form = RoomForm(request.POST, request.FILES)
        
        if form.is_valid():    
            usr = request.user
            room_number = form.cleaned_data["room_number"]
            number_of_students = form.cleaned_data["number_of_students"]
            status = form.cleaned_data["status"]
            room_cost = form.cleaned_data["room_cost"]
            room_imgs = form.cleaned_data["room_imgs"]

            room = Room(usr=usr,room_number=room_number,number_of_students=number_of_students,status=status,room_cost=room_cost,room_imgs=room_imgs)
            messages.success(request,"Room has been added.")
            
            room.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RoomForm()

    hostels = Hostel.objects.filter(usr=request.user)
    owner = OwnerDetail.objects.get(usr=request.user)
    context = {
        "form":form,
        "hostels":hostels,
        "owner":owner
    }

    return render(request,"hostelmanagement/dashboard/Inserts/roomsInsert.html",context)

def roomsUpdate(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)


    if request.method == "POST":     
        form = RoomForm(request.POST, request.FILES, instance=room)
        
        if form.is_valid():
            room.save()
            return HttpResponseRedirect('/dashboard/rooms/')
    else:
        form = RoomForm(instance=room)

    context = {
        "form":form,
    }

    return render(request,"hostelmanagement/dashboard/updates/roomsUpdate.html",context)

def roomsDelete(request, pk):
    data = Room.objects.get(id=pk)
    data.delete()
    return HttpResponseRedirect('/dashboard/rooms/')

def hostelDetails(request):
    if 'search-query' in request.GET:
        query = request.GET['search-query']
        print(query)
        searchData = Q(Q(near_by__icontains=query) | Q(security_deposit__icontains=query))
        data = HostelDetail.objects.filter(searchData)
    else:
        data = HostelDetail.objects.filter(usr=request.user)
    owner = OwnerDetail.objects.get(usr=request.user)

    context = {
        "hostelDetails":data,
        "owner":owner,
    }

    return render(request,"hostelmanagement/dashboard/hostelDetails.html",context)

def addDetails(request):
    if request.method == "POST":     
        form = HostelDetailsForm(request.POST)
        
        if form.is_valid():

            usr = request.user
            notice_period = form.cleaned_data["notice_period"]
            near_by = form.cleaned_data["near_by"]
            visitors_allowed = form.cleaned_data["visitors_allowed"]
            security_deposit = form.cleaned_data["security_deposit"]
            warden = form.cleaned_data["warden"]
            restrictions = form.cleaned_data["restrictions"]

            hostelDetail = HostelDetail(usr=usr,notice_period=notice_period,near_by=near_by,visitors_allowed=visitors_allowed,security_deposit=security_deposit,warden=warden,restrictions=restrictions)
            messages.success(request,"Profile Has Been Updated.")

            hostelDetail.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = HostelDetailsForm()
    owner = OwnerDetail.objects.get(usr=request.user)
    context = {
        "form":form,
        "owner":owner
    }

    return render(request,"hostelmanagement/dashboard/Inserts/addDetails.html",context)

def hostelDetailsUpdate(request, pk):
    room = HostelDetail.objects.get(id=pk)
    form = HostelDetailsForm(instance=room)


    if request.method == "POST":     
        form = HostelDetailsForm(request.POST, instance=room)
        
        if form.is_valid():
            room.save()
            return HttpResponseRedirect('/dashboard/hostel-details/')
    else:
        form = HostelDetailsForm(instance=room)

    context = {
        "form":form,
    }

    return render(request,"hostelmanagement/dashboard/updates/hostelDetailsUpdate.html",context)

def hostelDetailsDelete(request, pk):
    data = HostelDetail.objects.get(id=pk)
    data.delete()
    return HttpResponseRedirect('/dashboard/hostel-details/')

def facilities(request):
    if 'search-query' in request.GET:
        query = request.GET['search-query']
        data = Facilities.objects.filter(facility__icontains = query)
    else:
        data = Facilities.objects.all()
    owner = OwnerDetail.objects.get(usr=request.user)

    context = {
        "facilities": data,
        "owner":owner
    }

    return render(request,"hostelmanagement/dashboard/facilities.html",context)

def addFacility(request):
    if request.method == "POST":
        value = Facilities()
        value.facility = request.POST.get('facility')

        value.save()
        messages.success(request,"Facility Has Been Added.")
        return HttpResponseRedirect(request.path_info)
    owner = OwnerDetail.objects.get(usr=request.user)
    return render(request,"hostelmanagement/dashboard/Inserts/addFacility.html",{"owner":owner})
    
def facilitiesUpdate(request, pk):
    room = Facilities.objects.get(id=pk)
    form = FacilityForm(instance=room)


    if request.method == "POST":     
        form = FacilityForm(request.POST, instance=room)
        
        if form.is_valid():
            room.save()
            return HttpResponseRedirect('/dashboard/facilities/')
    else:
        form = FacilityForm(instance=room)

    context = {
        "form":form,
    }

    return render(request,"hostelmanagement/dashboard/updates/facilityUpdate.html",context)

def facilitiesDelete(request, pk):
    data = Facilities.objects.get(id=pk)
    data.delete()
    return HttpResponseRedirect('/dashboard/facilities/')

def ownerProfile(request):
    own1 = OwnerDetail.objects.get_or_create(usr=request.user)
    own = own1[0]
    print(own.address)
    if request.method == "POST":
        form = OwnerForm(request.POST, request.FILES, instance=own)
        
        if form.is_valid():
            own.name = form.cleaned_data["name"]
            own.address = form.cleaned_data["address"]
            own.contact_num = form.cleaned_data["contact_num"]
            own.profilePic = form.cleaned_data["profilePic"]
            own.save()
            return HttpResponseRedirect(request.path_info)

    else:
        form = OwnerForm(instance=own)
    
    context = {
        "form":form,
        "Owner":own
    }

    return render(request,"hostelmanagement/dashboard/ownerProfile.html",context)

