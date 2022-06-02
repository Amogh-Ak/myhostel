from django.contrib import admin
from .models import CustomUser, Facilities,HostelDetail, Hostel, OwnerDetail, Room, Reviews

# Register your models here.

class HostelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name",)}

admin.site.register(CustomUser)
admin.site.register(Hostel,HostelAdmin)
admin.site.register(HostelDetail)
admin.site.register(OwnerDetail)
admin.site.register(Facilities)
admin.site.register(Room)
admin.site.register(Reviews)