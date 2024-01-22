from django.db import models
import os
from django.conf import settings
from report_generator.screenshot.takeScreenshot import get_domain_from_url


class WebsiteReport(models.Model):
    url = models.URLField()
    screenshot = models.ImageField(upload_to='', blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    overall_rating = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    # Diagnostics
    cta_button_placement_rating = models.FloatField()
    cta_clarity_rating = models.FloatField()
    form_simplicity_rating = models.FloatField()
    form_autofill_rating = models.FloatField()
    messaging_clarity_rating = models.FloatField()
    headline_focus_rating = models.FloatField()
    offer_transparency_rating = models.FloatField()

    # Trust Signals
    social_proof = models.TextField()  # Testimonials, reviews, etc.
    company_info_presence = models.TextField()  # Company data, policies, etc.

    def save(self, *args, **kwargs):
        url_updated = get_domain_from_url(self.url)

        image_abs_path = os.path.join(settings.MEDIA_ROOT, f"{url_updated}.png")
        print(image_abs_path)
        # Check if the file exists
        if os.path.isfile(image_abs_path):
            print('Found the file')
            # Open the file and assign it to the screenshot field
            with open(image_abs_path, 'rb') as f:
                self.screenshot.save(f"{url_updated}.png", f, save=False)
                print('Saved the file')
        else:
            print('Did not find the file')

        super().save(*args, **kwargs)


