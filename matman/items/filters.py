import re

import django_filters
import django_filters.widgets
import django_filters.views
from taggit.models import Tag

from .models import Item, Scheme


class TagWidget(django_filters.widgets.CSVWidget):
    def value_from_datadict(self, data, files, name):
        value = super(django_filters.widgets.BaseCSVWidget, self).value_from_datadict(data, files, name)

        if value is not None:
            if value == "":  # empty value should parse as an empty list
                return []
            return re.findall('\w+', value)
        return None


class ItemFilter(django_filters.FilterSet):
    identifier = django_filters.CharFilter(lookup_expr='icontains', label='Identifier')
    serial_number = django_filters.CharFilter(lookup_expr='icontains', label='Serial Number')
    part_number = django_filters.CharFilter(lookup_expr='icontains', label='Part Number')
    manufacturer = django_filters.CharFilter(lookup_expr='icontains', label='Manufacturer')
    location = django_filters.CharFilter(lookup_expr='icontains', label='Location')
    tags__name = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__name',
        to_field_name='name',
        queryset=Tag.objects.all(),
        widget=TagWidget,
        label='Tags',
        conjoined=True,
    )
    is_active = django_filters.BooleanFilter()
    scheme = django_filters.ModelChoiceFilter(
        label='Scheme',
        queryset=Scheme.objects.all()
    )

    class Meta:
        model = Item
        fields = ['identifier', 'serial_number', 'part_number', 'manufacturer', 'location', 'tags__name']
