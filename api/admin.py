from django.contrib import admin
from .models import WebsiteReport

class WebsiteReportAdmin(admin.ModelAdmin):
    list_display = ('url', 'first_name', 'last_name', 'email', 'overall_grade', 'date')
    # Add other fields as needed

admin.site.register(WebsiteReport, WebsiteReportAdmin)