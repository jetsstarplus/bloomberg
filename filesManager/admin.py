from django.contrib import admin
from filesManager.models import Files, FileSetup, NumberSeries

# Register your models here.
class FileSetupAdmin(admin.ModelAdmin):
    list_display = ('ID','max_of_free_file_size','max_no_of_free_files','free_plan_restriction')
admin.site.register(FileSetup, FileSetupAdmin)

class FileAdmin(admin.ModelAdmin):
    list_display = ('user', 'file_name', 'file_size', 'date_created')
admin.site.register(Files, FileAdmin)

class NoSeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefix','suffix', 'last_date_used', 'last_no_used', 'default_no')
admin.site.register(NumberSeries, NoSeriesAdmin)