from django.contrib import admin
from .models import Post
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.gis.admin import GeoModelAdmin

class PostAdmin(GeoModelAdmin):
	list_display = ['title','location']
   
admin.site.register(Post,PostAdmin)

