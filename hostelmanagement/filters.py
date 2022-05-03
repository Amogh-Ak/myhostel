from dataclasses import fields
import django_filters
from hostelmanagement.models import *

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Hostel
        fields = ["location", "type_of_hostel"]