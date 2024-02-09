from django.db import models
import os
from django.conf import settings
from screenshot.takeScreenshot import get_domain_from_url, take_screenshot
from django.core.files import File


class WebsiteReport(models.Model):

    # Automatic Fields
    date = models.DateTimeField(auto_now_add=True)

    # Form Fields
    url = models.URLField()
    name_company = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    accept_terms = models.BooleanField(default=False)


    screenshot = models.ImageField(upload_to='', blank=True, null=True)

    # Overall Rating
    overall_rating = models.FloatField(blank=True, null=True)

    # Diagnostics
    cta_button_placement_diagnostics = models.CharField(blank=True, null=True, max_length=100)
    cta_clarity_diagnostics = models.CharField(blank=True, null=True, max_length=100)
    form_simplicity_diagnostics = models.CharField(blank=True, null=True, max_length=100)
    messaging_clarity_diagnostics = models.CharField(blank=True, null=True, max_length=100)
    headline_focus_diagnostics = models.CharField(blank=True, null=True, max_length=100)
    offer_transparency_diagnostics = models.CharField(blank=True, null=True, max_length=100)

    # Trust Signals
    social_proof = models.TextField(blank=True, null=True)  # Testimonials, reviews, etc.
    company_info_presence = models.TextField(blank=True, null=True)  # Company data, policies, etc.

    def save(self, *args, **kwargs):
        url_updated = get_domain_from_url(self.url)
        filename = f"{url_updated}.png"
        image_abs_path = os.path.join(settings.MEDIA_ROOT, filename)

        existing_entry = WebsiteReport.objects.filter(url=self.url).first()
        print(existing_entry)

        if not os.path.isfile(image_abs_path):
            print('Didnt find screenshot, taking a new screenshot')
            take_screenshot(self.url)



        # Check if the file exists
        if os.path.isfile(image_abs_path):
            print('Found the file')
            self.screenshot.name = f'{filename}'

            print('Assigned the existing file')

        super().save(*args, **kwargs)

