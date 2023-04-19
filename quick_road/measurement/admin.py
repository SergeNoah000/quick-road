from django.contrib import admin
from .models import Measurement

# Register your models here.


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    model =Measurement
    list_display= ('distance' ,'destination', 'location')
    
    
    