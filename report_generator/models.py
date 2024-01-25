from django.db import models
import os
from django.conf import settings
from screenshot.takeScreenshot import get_domain_from_url, take_screenshot
from django.core.files import File


class WebsiteReport(models.Model):
    url = models.URLField()
    screenshot = models.ImageField(upload_to='', blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    # Diagnostics
    overall_rating = models.FloatField(blank=True, null=True)
    cta_button_placement_rating = models.FloatField(blank=True, null=True)
    cta_clarity_rating = models.FloatField(blank=True, null=True)
    form_simplicity_rating = models.FloatField(blank=True, null=True)
    form_autofill_rating = models.FloatField(blank=True, null=True)
    messaging_clarity_rating = models.FloatField(blank=True, null=True)
    headline_focus_rating = models.FloatField(blank=True, null=True)
    offer_transparency_rating = models.FloatField(blank=True, null=True)

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

