from django.contrib import admin

from .models import Material, Department, Location, Borrow

admin.site.register(Material)
admin.site.register(Department)
admin.site.register(Location)
admin.site.register(Borrow)
