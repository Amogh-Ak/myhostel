from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("hostelmanagement.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'hostelmanagement.views.error_404_view'
handler500 = 'hostelmanagement.views.error_500_view'