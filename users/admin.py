from django.contrib import admin
from .models import Profile,Prod,ProdImage,Service,Review,Message
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import User
from django.contrib.gis.admin import GeoModelAdmin

class ServiceAdmin(GeoModelAdmin):
	list_display = ['name_business','location']
   
admin.site.register(Service,ServiceAdmin)

admin.site.register(Profile)

admin.site.register(Message)
class UserAdmin(GeoModelAdmin):
	list_display = ['username','geo_location','Latitude','Longitude']
   
admin.site.register(User,UserAdmin)
admin.site.register(Review)

class ProdImageAdmin(admin.StackedInline):
    model = ProdImage

class ProdAdmin(GeoModelAdmin):
	list_display = ['Title','location']
   
admin.site.register(Prod,ProdAdmin)
class PostAdmin(admin.ModelAdmin):
    inlines = [ProdImageAdmin]

    class Meta:
       model = Prod

@admin.register(ProdImage)
class ProdImageAdmin(admin.ModelAdmin):
    pass